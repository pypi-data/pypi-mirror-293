// This file is part of the mlhp project. License: See LICENSE

#include "mlhp/core/sparse.hpp"
#include "mlhp/core/algorithm.hpp"
#include "mlhp/core/memory.hpp"
#include "mlhp/core/dense.hpp"
#include "mlhp/core/parallel.hpp"
#include "mlhp/core/logging.hpp"

#include <numeric>
#include <string>

namespace mlhp::linalg
{

AbsSparseMatrix::AbsSparseMatrix( ) :
    indices_( nullptr ), indptr_( new SparsePtr[1] { 0 } ), data_( nullptr ),
    size1_( 0 ), size2_( 0 )
{ }

//AbsSparseMatrix::AbsSparseMatrix( SparseInternalDataStructure data,
//                                  size_t size1, size_t size2 ) :
//    indices_( std::get<0>( data ) ), 
//    indptr_( std::get<1>( data ) ), 
//    data_( std::get<2>( data ) ),
//    size1_( 0 ), size2_( 0 )
//{ }

void AbsSparseMatrix::claim( SparseDataStructure data, 
                             SparseIndex size1, 
                             SparseIndex size2 )
{
    cleanup( );

    indices_ = std::get<0>( data );
    indptr_ = std::get<1>( data );
    data_ = std::get<2>( data );
    size1_ = size1;
    size2_ = size2;
}


SparseDataStructure AbsSparseMatrix::release( )
{
    SparseDataStructure sparseDataStructure { indices_, indptr_, data_ };

    indices_ = nullptr;
    indptr_ = nullptr;
    data_ = nullptr;

    size1_ = 0;
    size2_ = 0;

    return sparseDataStructure;
}

SparsePtr AbsSparseMatrix::nnz( ) const
{
    return indptr_[size1_];
}

SparseIndex AbsSparseMatrix::size1( ) const
{
    return size1_;
}

SparseIndex AbsSparseMatrix::size2( ) const
{
    return size2_;
}


void AbsSparseMatrix::copyAssign( const AbsSparseMatrix& other )
{
    cleanup( );

    auto indices = other.indices( );
    auto indptr = other.indptr( );
    auto data = other.data( );

    auto size1 = other.size1( );
    auto size2 = other.size2( );

    auto newIndices = new SparseIndex[other.nnz( )];
    auto newIndptr = new SparsePtr[size1 + 1];
    auto newData = new double[other.nnz( )];

    std::copy( indices, indices + other.nnz( ), newIndices );
    std::copy( indptr, indptr + size1 + 1, newIndptr );
    std::copy( data, data + other.nnz( ), newData );

    claim( { newIndices, newIndptr, newData }, size1, size2 );
}

void AbsSparseMatrix::moveAssign( AbsSparseMatrix&& other )
{
    cleanup( );

    auto size1 = other.size1( );
    auto size2 = other.size2( );

    this->claim( other.release( ), size1, size2 );
}

void AbsSparseMatrix::cleanup( )
{
    delete[] indices_;
    delete[] indptr_;
    delete[] data_;

    indices_ = nullptr;
    indptr_ = nullptr;
    data_ = nullptr;

    size1_ = 0;
    size2_ = 0;
}

double AbsSparseMatrix::operator ()( size_t i,
                                     size_t j ) const
{
    auto result = std::find( indices_ + indptr_[i], indices_ + indptr_[i + 1], j );

    if( result != indices_ + indptr_[i + 1] )
    {
        return data_[std::distance( indices_, result )];
    }

    return 0.0;
}

double* AbsSparseMatrix::find( size_t i, size_t j )
{
    auto result = std::find( indices_ + indptr_[i], indices_ + indptr_[i + 1], j );

    return result != indices_ + indptr_[i + 1] ? &data_[std::distance( indices_, result )] : nullptr;
}

const double* AbsSparseMatrix::find( size_t i, size_t j ) const
{
    return const_cast<AbsSparseMatrix*>( this )->find( i, j );
}

std::vector<double> AbsSparseMatrix::operator*( const std::vector<double>& vector ) const
{
    MLHP_CHECK( vector.size( ) == size2_, "Inconsistent sizes in matrix vector multiplication." );

    std::vector<double> result( size1_, 0.0 );

    multiply( &vector[0], &result[0] );

    return result;
}

AbsSparseMatrix::~AbsSparseMatrix( )
{
    cleanup( );
}

size_t AbsSparseMatrix::memoryUsage( ) const
{
    return ( sizeof( *data_ ) + sizeof( *indices_ ) ) * nnz( ) + sizeof( *indptr_ ) * ( size1( ) + 1 );
}

UnsymmetricSparseMatrix& UnsymmetricSparseMatrix::operator=( const UnsymmetricSparseMatrix& other )
{
    copyAssign( other );

    return *this;
}

UnsymmetricSparseMatrix::UnsymmetricSparseMatrix( const UnsymmetricSparseMatrix& other ) :
    UnsymmetricSparseMatrix( )
{
    *this = other;
}

UnsymmetricSparseMatrix::UnsymmetricSparseMatrix( UnsymmetricSparseMatrix&& other )
{
    *this = std::move( other );
}

UnsymmetricSparseMatrix& UnsymmetricSparseMatrix::operator=( UnsymmetricSparseMatrix&& other )
{
    moveAssign( std::move( other ) );

    return *this;
}

SymmetricSparseMatrix& SymmetricSparseMatrix::operator=( const SymmetricSparseMatrix& other )
{
    copyAssign( other );

    return *this;
}

SymmetricSparseMatrix::SymmetricSparseMatrix( const SymmetricSparseMatrix& other )
{
    *this = other;
}


SymmetricSparseMatrix::SymmetricSparseMatrix( SymmetricSparseMatrix&& other )
{
    *this = std::move( other );
}

SymmetricSparseMatrix& SymmetricSparseMatrix::operator=( SymmetricSparseMatrix&& other )
{
    moveAssign( std::move( other ) );

    return *this;
}

namespace detail
{

inline auto swapIndices( size_t i, size_t j )
{
    return i > j ? std::array<size_t, 2> { j, i } : std::array<size_t, 2> { i, j };
}

} // namespace detail

double SymmetricSparseMatrix::operator()( size_t i, size_t j ) const
{
    auto [I, J] = detail::swapIndices( i, j );

    return AbsSparseMatrix::operator()( I, J );
}

double* SymmetricSparseMatrix::find( size_t i, size_t j )
{
    auto [I, J] = detail::swapIndices( i, j );

    return AbsSparseMatrix::find( I, J );
}

namespace detail
{

void addVectors( const double* MLHP_RESTRICT a,
                 double factorB,
                 const double* MLHP_RESTRICT b,
                 double* MLHP_RESTRICT target,
                 size_t n )
{
    #pragma omp parallel for schedule( dynamic, 2048 )
    for( std::int64_t i = 0; i < static_cast<std::int64_t>( n ); ++i )
    {
        target[i] = a[i] + factorB * b[i];
    }
}

void subtractVectors( const double* MLHP_RESTRICT a, 
                      const double* MLHP_RESTRICT b, 
                      double* MLHP_RESTRICT target, 
                      size_t n )
{
    #pragma omp parallel for schedule( dynamic, 2048 )
    for( std::int64_t i = 0; i < static_cast<std::int64_t>( n ); ++i )
    {
        target[i] = a[i] - b[i];
    }
}

void subtractVectors( const double* MLHP_RESTRICT a,
                      double factorB,
                      const double* MLHP_RESTRICT b,
                      double* MLHP_RESTRICT target,
                      size_t n )
{
    #pragma omp parallel for schedule( dynamic, 2048 )
    for( std::int64_t i = 0; i < static_cast<std::int64_t>( n ); ++i )
    {
        target[i] = a[i] - factorB * b[i];
    }
}

void addVectorsInPlace( double* MLHP_RESTRICT a, const double* MLHP_RESTRICT b, double factor, size_t n )
{
    #pragma omp parallel for schedule( dynamic, 2048 )
    for( std::int64_t i = 0; i < static_cast<std::int64_t>( n ); ++i )
    {
        a[i] += factor * b[i];
    }
}

void multiplyVectorByScalar( double* vector, double scalar, size_t n )
{
    #pragma omp parallel for schedule( dynamic, 2048 )
    for( std::int64_t i = 0; i < static_cast<std::int64_t>( n ); ++i )
    {
        vector[i] *= scalar;
    }
}

void multiplyVectorByScalar( const double* MLHP_RESTRICT vector, double scalar, size_t n, double* MLHP_RESTRICT target )
{
    #pragma omp parallel for schedule( dynamic, 2048 )
    for( std::int64_t i = 0; i < static_cast<std::int64_t>( n ); ++i )
    {
        target[i] = vector[i] * scalar;
    }
}

MLHP_PURE 
double innerProduct( const double* MLHP_RESTRICT v1, const double* MLHP_RESTRICT v2, size_t n )
{
    double result = 0.0;

    #pragma omp parallel for schedule( dynamic, 2048 ) reduction(+:result)
    for( std::int64_t i = 0; i < static_cast<std::int64_t>( n ); ++i )
    {
        result += v1[i] * v2[i];

    } // for i

    return result;
}

void setVectorTo( double* MLHP_RESTRICT target, double value, size_t n )
{
    #pragma omp parallel for schedule( dynamic, 2048 )
    for( std::int64_t i = 0; i < static_cast<std::int64_t>( n ); ++i )
    {
        target[i] = value;
    }
}

MLHP_PURE 
double vectorNormSquared( const double* vector, size_t n )
{
    double result = 0.0;

    #pragma omp parallel for schedule( dynamic, 2048 ) reduction(+:result)
    for( std::int64_t i = 0; i < static_cast<std::int64_t>( n ); ++i )
    {
        result += vector[i] * vector[i];
    }

    return result;
}

MLHP_PURE 
double vectorNorm( const double* vector, size_t n )
{
    return std::sqrt( vectorNormSquared( vector, n ) );
}

void arnoldi( const LinearOperator& multiply,
              const std::vector<std::vector<double>>& Q,
              size_t k,
              size_t n,
              double* MLHP_RESTRICT h,
              double* MLHP_RESTRICT q )
{
    multiply( &Q[k][0], q );

    for( size_t i = 0; i < k + 1; ++i )
    {
        h[i] = std::inner_product( q, q + n, &Q[i][0], double( 0.0 ) );

        // q += -h[i] * Q[i]
        addVectorsInPlace( q, &Q[i][0], -h[i], n );
    }

    h[k + 1] = vectorNorm( q, n );

    multiplyVectorByScalar( q, 1.0 / h[k + 1], n );
}

std::array<double, 2> givens_rotation( double v1, double v2 )
{
    if( v1 == 0 )
    {
        return { 0.0, 1.0 };
    }
    else
    {
        double t = std::sqrt( v1 * v1 + v2 * v2 );
        double cs = std::abs( v1 ) / t;
        double sn = cs * v2 / v1;

        return { cs, sn };
    }
}

std::array<double, 2> apply_givens_rotation( double* MLHP_RESTRICT h,  // m
                                             double* MLHP_RESTRICT cs, // m
                                             double* MLHP_RESTRICT sn, // m
                                             size_t k )
{
    // Apply for ith column
    for( size_t i = 0; i < k; ++i )
    {
        double tmp = cs[i] * h[i] + sn[i] * h[i + 1];

        h[i + 1] = -sn[i] * h[i] + cs[i] * h[i + 1];

        h[i] = tmp;
    }

    // Update the next sin cos values for rotation
    auto [cs_k, sn_k] = givens_rotation( h[k], h[k + 1] );

    // Eliminate H( i + 1, i )
    h[k] = cs_k * h[k] + sn_k * h[k + 1];

    h[k + 1] = 0.0;

    return { cs_k, sn_k };
}

} // namespace detail

void UnsymmetricSparseMatrix::multiply( const double* vector, double* target ) const
{
    double* MLHP_RESTRICT t = target;
    double* MLHP_RESTRICT data = this->data( );
    const auto* MLHP_RESTRICT v = vector;
    const auto* MLHP_RESTRICT indptr = this->indptr( );
    const auto* MLHP_RESTRICT indices = this->indices( );

    auto size = this->size1( );

    detail::setVectorTo( t, 0.0, size );

    #pragma omp parallel for schedule( dynamic, 1024 )
    for( std::int64_t iInt = 0; iInt < static_cast<std::int64_t>( size ); ++iInt )
    {
        size_t i = static_cast<size_t>( iInt );

        for( auto j = indptr[i]; j < indptr[i + 1]; ++j )
        {
            t[i] += data[j] * v[indices[j]];
        }
    }
}

void SymmetricSparseMatrix::multiply( const double* vector, double* target ) const
{
    double* MLHP_RESTRICT t = target;
    double* MLHP_RESTRICT dataPtr = this->data( );
    const auto* MLHP_RESTRICT rhs = vector;
    const auto* MLHP_RESTRICT columnIndices = this->indices( );
    const auto* MLHP_RESTRICT rowPtr = this->indptr( );

    detail::setVectorTo( t,  0.0,  this->size1( ) );

    //#pragma omp parallel for schedule( dynamic, 512 )
    for( std::int64_t i = 0; i < static_cast<std::int64_t>( this->size1( ) ); ++i )
    {
        double rhsI = rhs[i];
        double value1 = dataPtr[rowPtr[i]] * rhs[i];

        for( auto index = rowPtr[i] + 1; index < rowPtr[i + 1]; ++index )
        {
            auto j = columnIndices[index];

            value1 += dataPtr[index] * rhs[j];

            auto value2 = dataPtr[index] * rhsI;

            //#pragma omp atomic
            t[j] += value2;
        }

        //#pragma omp atomic
        t[i] += value1;
    }
}

namespace
{

void printMatrix( const AbsSparseMatrix& matrix, const char type[], std::ostream& os )
{
    auto fillRatio = static_cast<double>( matrix.nnz( ) );
    
    if( matrix.symmetricHalf( ) )
    {
        auto diagcount = size_t { 0 };

        for( size_t ii = 0; ii < matrix.size1( ); ++ii )
        {
            diagcount += matrix.find( ii, ii ) != nullptr;
        }

        fillRatio = 2.0 * fillRatio - diagcount;
    }

    fillRatio /=  matrix.size1( ) * matrix.size2( );

    os << type << "SparseMatrix (address: " << &matrix << ")\n";
    os << "    size               : (" << matrix.size1( ) << ", " << matrix.size2( ) << ")\n";
    os << "    number of nonzeros : " << matrix.nnz( ) << "\n";
    os << "    fill ratio         : " << utilities::roundNumberString( 100.0 * fillRatio ) << " %" << std::endl;
    os << "    heap memory usage  : " << utilities::memoryUsageString( matrix.memoryUsage( ) );
    os << std::endl;
}

} // namespace

void print( const AbsSparseMatrix& matrix, std::ostream& os )
{
    printMatrix( matrix, "Abs", os );
}

void print( const UnsymmetricSparseMatrix& matrix, std::ostream& os )
{
    printMatrix( matrix, "Unsymmetric", os );
}

void print( const SymmetricSparseMatrix& matrix, std::ostream& os )
{
    printMatrix( matrix, "Symmetric", os );
}

size_t IterativeSolverInfo::niterations( ) const
{
    auto size = residualNorms_.size( );

    return size > 0 ? size - 1 : 0;
}

//function[x, e] = gmres( A, b, x, max_iterations, threshold )
std::vector<double> gmresRestrict( const LinearOperator& multiply,
                                   const double* MLHP_RESTRICT b,
                                   double* MLHP_RESTRICT x,
                                   size_t size,
                                   size_t max_iterations,
                                   double threshold )
{
    size_t n = size;

    size_t m = max_iterations;

    double* MLHP_RESTRICT r = new double[n];
    double* MLHP_RESTRICT tmp = new double[n];

    multiply( x, tmp );

    detail::subtractVectors( b, tmp, r, n );

    double b_norm = detail::vectorNorm( b, n );

    if( b_norm == 0.0 )
    {
        std::fill( x, x + n, 0.0 );

        return { };
    }

    double error = detail::vectorNorm( r, n ) / b_norm;

    size_t max = m + 1 > n ? m + 1 : n;

    double* MLHP_RESTRICT sn = new double[m];
    double* MLHP_RESTRICT cs = new double[m];
    double* MLHP_RESTRICT beta = new double[max];

    std::fill( sn, sn + m, 0.0 );
    std::fill( cs, cs + m, 0.0 );
    std::fill( beta, beta + max, 0.0 );
    
    std::vector<double> e = { error };

    double r_norm = detail::vectorNorm( r, n );

    beta[0] = r_norm;

    std::vector<std::vector<double>> Q, H;

    Q.emplace_back( n, 0.0 );

    detail::multiplyVectorByScalar( r, 1.0 / r_norm, n, &Q.back( )[0] );

    size_t k = 0;

    for( ; k < m; ++k )
    {
        Q.emplace_back( n, 0.0 );
        H.emplace_back( k + 2, 0.0 );

        detail::arnoldi( multiply, Q, k, n, &H[k][0], &Q[k + 1][0] );

        // Eliminate the last element in H ith row and update the rotation matrix
        auto result = detail::apply_givens_rotation( &H[k][0], cs, sn, k );

        cs[k] = result[0];
        sn[k] = result[1];

        beta[k + 1] = -sn[k] * beta[k];
        beta[k] *= cs[k];

        error = std::abs( beta[k + 1] ) / b_norm;

        e.push_back( error );

        if( error <= threshold )
        {
            ++k;
            break;
        }
    }

    delete[] r;
    delete[] tmp;
    delete[] sn;
    delete[] cs;

    std::vector<double> y( k, 0.0 );

    // Backward substitution
    for( size_t index = 0; index < k; ++index )
    {
        size_t i = k - index - 1;

        double factor = H[i][i];

        y[i] = beta[i] / factor;

        for( size_t j = k - index; j < k; ++j )
        {
            y[i] -= y[j] * H[j][i] / factor;
        }
    }

    delete[] beta;

    for( size_t i = 0; i < k; ++i )
    {
        for( size_t j = 0; j < n; ++j )
        {
            x[j] += Q[i][j] * y[i];
        }
    }

    return e;
}

std::vector<double> gmres( const LinearOperator& multiply,
                           const double* rhs,
                           double* solution,
                           size_t systemSize,
                           [[maybe_unused]]size_t maximumNumberOfIterations,
                           double threshold )
{
    //return gmresRestrict( multiply, rhs, solution, systemSize, maximumNumberOfIterations, threshold );
    
    size_t reset = 1000000;

    auto errors = gmresRestrict( multiply, rhs, solution, systemSize, reset, threshold );

    auto allErrors = errors;

    while( errors.size( ) == reset + 1 )
    {
        errors = gmresRestrict( multiply, rhs, solution, systemSize, reset, threshold );

        allErrors.insert( allErrors.end( ), errors.begin( ), errors.end( ) );

        //std::cout << "resetting ... (error = " << errors.back( ) << ")" << std::endl;
    }

    return allErrors;
}

std::vector<double> cg( const LinearOperator& multiply,
                        const std::vector<double>& b,
                        std::vector<double>& solution,
                        const LinearOperator& preconditioner,
                        size_t maximalNumberOfIterations,
                        double tolerance )
{
    size_t numberOfUnknowns = b.size( );

    double toleranceSquared = tolerance * tolerance;

    solution.resize( numberOfUnknowns );

    detail::setVectorTo( solution.data( ), 0.0, solution.size( ) );

    std::vector<double> Adi( numberOfUnknowns );
    std::vector<double> preconditionedResidual( numberOfUnknowns );
    std::vector<double> preconditionedRightHandSide( numberOfUnknowns );

    auto residual = b; // - A * solution

    preconditioner( residual.data( ), preconditionedResidual.data( ) );

    auto direction = preconditionedResidual;

    std::vector<double> errors = { detail::innerProduct( residual.data( ), preconditionedResidual.data( ), numberOfUnknowns ) };

    if( errors.back( ) > toleranceSquared )
    {
        preconditioner( b.data( ), preconditionedRightHandSide.data( ) );

        for ( size_t iter = 0; iter <= maximalNumberOfIterations; ++iter )
        {
            // compute Adi = A * direction;
            detail::setVectorTo( Adi.data( ), 0.0, Adi.size( ) );

            multiply( direction.data( ), Adi.data( ) );

            // compute directionT*A*direction
            double diTAdi = detail::innerProduct( direction.data( ), Adi.data( ), numberOfUnknowns );

            // compute riT*ri / diT*A*di
            double alpha = errors.back( ) / diTAdi;

            detail::addVectorsInPlace( solution.data( ), direction.data( ), alpha, numberOfUnknowns );
            detail::addVectorsInPlace( residual.data( ), Adi.data( ), -alpha, numberOfUnknowns );

            // computePreConditionedResidual
            preconditioner( residual.data( ), preconditionedResidual.data( ) );

            errors.push_back( detail::innerProduct( residual.data( ), preconditionedResidual.data( ), numberOfUnknowns ) );

            if( errors.back( ) <= toleranceSquared )
            {
                return errors;
            }

            // compute ri+1Tri+1 / riTri
            double beta = errors[errors.size( ) - 1] / errors[errors.size( ) - 2];

            // update search direction:  direction = preconditioned residual + beta * direction;
            detail::multiplyVectorByScalar( direction.data( ), beta, numberOfUnknowns );
            detail::addVectorsInPlace( direction.data( ), preconditionedResidual.data( ), 1.0, numberOfUnknowns );
        } // end of iter-loop

        std::cout << "Solution not converged after " + std::to_string( maximalNumberOfIterations ) +
                     " iterations. Matrix is possibly singular or not positive definite" << std::endl;
    }

    return errors;
}

std::vector<double> bicgstab( const LinearOperator& multiply,
                              const std::vector<double>& b,
                              std::vector<double>& x,
                              const LinearOperator& preconditioner,
                              size_t maximumNumberOfIterations,
                              double tolerance )
{
    std::uint64_t n = b.size( );

    x.resize( n );
    
    detail::setVectorTo( x.data( ), 0.0, n );

    std::vector<double> r( n ), tmp( n );

    // r = b - A * x
    multiply( x.data( ), tmp.data( ) );
    detail::subtractVectors( b.data( ), tmp.data( ), r.data( ), n );

    auto r0 = r;

    double bNorm2 = detail::vectorNormSquared( b.data( ), n );

    if( bNorm2 == 0.0 )
    {
        return { 0.0 };
    }

    double rho = 1.0;
    double alpha = 1.0;
    double omega = 1.0;

    auto residualNorm = [&]( ) { return std::sqrt( detail::vectorNormSquared( r.data( ), n ) / bNorm2 ); };

    std::vector<double> v( n, 0.0 ), p( n, 0.0 );
    std::vector<double> y( n ), z( n ), s( n ), t( n );
    
    std::vector<double> residualNorms { residualNorm( ) };

    for( size_t it = 0; it < maximumNumberOfIterations && residualNorms.back( ) > tolerance; ++it )
    {
        double previousRho = rho;

        rho = detail::innerProduct( r0.data( ), r.data( ), n );

        double beta = ( rho / previousRho ) * ( alpha / omega );

        // p = r + beta * ( p - omega * v );
        detail::subtractVectors( p.data( ), omega, v.data( ), tmp.data( ), n );
        detail::addVectors( r.data( ), beta, tmp.data( ), p.data( ), n );

        // y = K(p)
        preconditioner( p.data( ), y.data( ) );

        // v = A*y
        multiply( y.data( ), v.data( ) );

        // alpha = rho / (r0, v)
        alpha = rho / detail::innerProduct( r0.data( ), v.data( ), n );

        // x += y * alpha (originally called h)
        detail::addVectorsInPlace( x.data( ), y.data( ), alpha, n );

        // s = r - alpha * v
        detail::subtractVectors( r.data( ), alpha, v.data( ), s.data( ), n );

        // z = K( s )
        preconditioner( s.data( ), z.data( ) );

        // t = A*z
        multiply( z.data( ), t.data( ) );

        // (t, s) / (t, t)
        double ts = detail::innerProduct( t.data( ), s.data( ), n );
        double tt = detail::vectorNormSquared( t.data( ), n );

        omega = tt > 0.0 ? ts / tt : 0.0;

        // x += omega * z;
        detail::addVectorsInPlace( x.data( ), z.data( ), omega, n );

        // r = s - omega * t;
        detail::subtractVectors( s.data( ), omega, t.data( ), r.data( ), n );

        residualNorms.push_back( residualNorm( ) );
    }

    if( residualNorms.size( ) >= maximumNumberOfIterations )
    {
        std::cout << "Solution not converged after " + std::to_string( maximumNumberOfIterations ) +
                     " iterations. Matrix is possibly singular or not positive definite" << std::endl;
    }

    return residualNorms;
}

LinearOperator makeDefaultMultiply( const AbsSparseMatrix& matrix )
{
    return [&]( const double* vector, double* target )
    {
        matrix.multiply( vector,  target );
    };
}

LinearOperator makeNoPreconditioner( size_t size )
{
    return [=]( const double* vector, double* target )
    {
        std::copy( vector, vector + size, target );
    };
}

LinearOperator makeDiagonalPreconditioner( const AbsSparseMatrix& matrix )
{
    size_t size = matrix.size1( );

    std::vector<double> diagonal( size );

    #pragma omp parallel for schedule( dynamic, 2048 )
    for( std::int64_t iInt = 0; iInt < static_cast<std::int64_t>( size ); ++iInt )
    {
        auto i = static_cast<size_t>( iInt );
        auto v = matrix( i, i );

        MLHP_CHECK( std::abs( v ) > 100.0 * std::numeric_limits<double>::min( ),
            "Encountered zero matrix diagonal entry in diagonal preconditioner." );

        diagonal[i] = 1.0 / v;
    }

    return [size, diagonal]( const double* vector, double* target ) noexcept
    {
        double* MLHP_RESTRICT targetPtr = target;
        const double* MLHP_RESTRICT vectorPtr = vector;
        const double* MLHP_RESTRICT diagonalPtr = diagonal.data( );

        #pragma omp parallel for schedule( dynamic, 2048 )
        for( std::int64_t i = 0; i < static_cast<std::int64_t>( size ); ++i )
        {
            targetPtr[i] = vectorPtr[i] * diagonalPtr[i];
        }
    };
}

namespace detail
{

template<typename MatrixType>
auto copyZero( const MatrixType& matrix )
{
    auto newIndices = new SparseIndex[matrix.nnz( )];
    auto newIndptr = new SparsePtr[matrix.size1( ) + 1];
    auto newData = new double[matrix.nnz( )];

    std::copy( matrix.indices( ), matrix.indices( ) + matrix.nnz( ), newIndices );
    std::copy( matrix.indptr( ), matrix.indptr( ) + matrix.size1( ) + 1, newIndptr );
    std::fill( newData, newData + matrix.nnz( ), 0.0 );

    MatrixType newMatrix;

    newMatrix.claim( { newIndices, newIndptr, newData }, matrix.size1( ), matrix.size2( ) );

    return newMatrix;
}

void reduceAndSort( const std::vector<SparseIndex>& reducedDofsMap,
                    std::vector<SparseIndex>& group )
{
    std::transform( group.begin( ), group.end( ), group.begin( ),
                    [&]( auto value ){ return reducedDofsMap[value]; } );

    std::sort( group.begin( ), group.end( ) );

    auto newEnd = std::find( group.begin( ), group.end( ), NoValue<SparseIndex> );

    group.erase( newEnd, group.end( ) );
}

template<typename Operation>
void accessGroup( const UnsymmetricSparseMatrix& matrix,
                  const std::vector<SparseIndex>& group,
                  Operation&& operation )
{
    auto indices = matrix.indices( );
    auto indptr = matrix.indptr( );
    auto data = matrix.data( );

    for( auto globalI : group )
    {
        auto* current = indices + indptr[globalI];

        for( auto globalJ : group )
        {
            current = std::find( current, indices + indptr[globalI + 1], globalJ );

            MLHP_CHECK_DBG( *current == globalJ, "Entry not in sparse matrix!" );

            operation( data[std::distance( indices, current )] );

            current++;
        } // for index j
    } // for i
}

void extractSorted( const UnsymmetricSparseMatrix& matrix, 
                    const std::vector<SparseIndex>& group,
                    std::vector<double>& target )
{
    target.resize( 0 );

    auto operation = [&]( double value ) { target.push_back( value ); };

    accessGroup( matrix, group, operation );
}

void scatterSorted( const UnsymmetricSparseMatrix& matrix,
                    const std::vector<SparseIndex>& group,
                    const std::vector<double>& inverse )
{
    auto* MLHP_RESTRICT ptr = inverse.data( );

    auto operation = [&]( double& target )
    {
        double value = *( ptr++ );

        #pragma omp atomic
        target += value;
    };

    accessGroup( matrix, group, operation );
}

} // namespace detail

linalg::UnsymmetricSparseMatrix makeAdditiveSchwarzPreconditioner( const UnsymmetricSparseMatrix& matrix,
                                                                   const IndexSetRange& groups,
                                                                   const std::vector<SparseIndex>& exclude,
                                                                   SparseIndex allNDof )
{
    auto ngroups = groups.size( );
    
    auto preconditioner = detail::copyZero<UnsymmetricSparseMatrix>( matrix );

    auto boundaryDofMap = algorithm::backwardIndexMap<SparseIndex>(
        algorithm::indexMask( exclude, allNDof ), true );

    #pragma omp parallel
    {
        std::vector<double> Ke, inverse;
        std::vector<size_t> permutation;
        std::vector<SparseIndex> group;

        #pragma omp for
        for( std::int64_t iGroupInt = 0; iGroupInt < static_cast<std::int64_t>( ngroups ); ++iGroupInt )
        {
            auto iGroup = static_cast<size_t>( iGroupInt );

            utilities::resize0( group );

            // Prepare location map / index set
            groups( iGroup, group );

            detail::reduceAndSort( boundaryDofMap, group );

            // Extract element / group matrix
            detail::extractSorted( matrix, group, Ke );

            // Invert matrix
            permutation.resize( group.size( ) );
            inverse.resize( group.size( ) * group.size( ) );

            lu( Ke.data( ), permutation.data( ), group.size( ) );
            luInvert( Ke.data( ), permutation.data( ), group.size( ), inverse.data( ) );

            // Scatter into preconditioner
            detail::scatterSorted( preconditioner, group, inverse );
        }
    }

    return preconditioner;
}


template<typename TargetType, typename SourceType>
TargetType convertSparseMatrix( const SourceType& matrix )
{
    MLHP_CHECK( matrix.size1( ) == matrix.size2( ), "" );

    auto size = matrix.size1( );

    constexpr auto symmetricSource = std::is_same_v<SourceType, SymmetricSparseMatrix>;

    auto nnz = symmetricSource ? ( 2 * matrix.nnz( ) - size ) : ( matrix.nnz( ) + size ) / 2;

    auto oldIndices = matrix.indices( );
    auto oldIndptr = matrix.indptr( );
    auto oldData = matrix.data( );

    auto newIndices = new SparseIndex[nnz];
    auto newIndptr = new SparsePtr[size + 1];
    auto newData = new double[nnz];

    newIndptr[0] = 0;

    if constexpr( symmetricSource )
    {
        std::vector<size_t> nentries( size, 0 );

        for( size_t iRow = 0; iRow < size; ++iRow )
        {
            nentries[iRow]++;

            for( auto index = oldIndptr[iRow] + 1; index < oldIndptr[iRow + 1]; ++index )
            {
                nentries[iRow]++;
                nentries[oldIndices[index]]++;
            }
        }

        std::partial_sum( nentries.begin( ), nentries.end( ), newIndptr + 1 );
        std::fill( nentries.begin( ), nentries.end( ), 0 );

        // Could be parallel, but needs omp atomic and rows need to be sorted again
        for( SparseIndex iRow = 0; iRow < size; ++iRow )
        {
            auto newBegin = newIndptr[iRow] + nentries[iRow];

            newIndices[newBegin] = iRow;
            newData[newBegin] = oldData[oldIndptr[iRow]];

            auto rowLength = oldIndptr[iRow + 1] - oldIndptr[iRow];

            for( size_t jEntry = 1; jEntry < rowLength; ++jEntry )
            {
                auto iColumn = oldIndices[oldIndptr[iRow] + jEntry];
                auto value = oldData[oldIndptr[iRow] + jEntry];

                newIndices[newBegin + jEntry] = iColumn;
                newIndices[newIndptr[iColumn] + nentries[iColumn]] = iRow;

                newData[newBegin + jEntry] = value;
                newData[newIndptr[iColumn] + nentries[iColumn]] = value;

                nentries[iColumn]++;
            }
        }
    }
    else
    {
        size_t index = 0;

        // Could probably also somehow be parallel
        for( size_t iRow = 0; iRow < size; ++iRow )
        {
            auto end = oldIndices + oldIndptr[iRow + 1];
            auto start = std::lower_bound( oldIndices + oldIndptr[iRow], end, iRow );

            for( auto column = start; column < end; ++column )
            {
                newIndices[index] = *column;
                newData[index] = oldData[std::distance( oldIndices, column )];

                index++;
            }

            newIndptr[iRow + 1] = index;
        }
    }

    TargetType result;

    result.claim( { newIndices, newIndptr, newData }, size, size );

    return result;
}

SymmetricSparseMatrix convertToSymmetric( const UnsymmetricSparseMatrix& matrix )
{
    return convertSparseMatrix<SymmetricSparseMatrix>( matrix );
}

UnsymmetricSparseMatrix convertToUnsymmetric( const SymmetricSparseMatrix& matrix )
{
    return convertSparseMatrix<UnsymmetricSparseMatrix>( matrix );
}

IterativeSolverWithWithInfo makeCGSolverWithInfo( double tolerance, 
                                                  size_t maxiterations )
{
    auto info = std::make_shared<IterativeSolverInfo>( );

    std::function solver = [=]( const AbsSparseMatrix& matrix,
                                const std::vector<double>& rhs )
    {
        auto multiply = makeDefaultMultiply( matrix );
        auto preconditioner = makeDiagonalPreconditioner( matrix );
        auto niterations = maxiterations != NoValue<size_t> ? maxiterations : matrix.size1( );
        auto solution = std::vector<double> { };

        info->residualNorms_ = cg( multiply, rhs, solution, preconditioner, niterations, tolerance );

        return solution;
    };

    return std::make_tuple( solver, info );
}

SparseSolver makeCGSolver( double tolerance, 
                           size_t maxiterations )
{
    return std::get<0>( makeCGSolverWithInfo( tolerance, maxiterations ) );
}

IterativeSolverWithWithInfo makeBiCGStabSolverWithInfo( double tolerance )
{
    auto info = std::make_shared<IterativeSolverInfo>( );

    std::function solver = [=]( const AbsSparseMatrix& matrix,
                                const std::vector<double>& rhs )
    {
        auto multiply = makeDefaultMultiply( matrix );
        auto preconditioner = makeDiagonalPreconditioner( matrix );

        std::vector<double> solution;

        info->residualNorms_ = bicgstab( multiply, rhs, solution, preconditioner, matrix.size1( ), tolerance );

        return solution;
    };

    return std::make_tuple( solver, info );
}

MLHP_EXPORT
SparseSolver makeBiCGStabSolver( double tolerance )
{
    return std::get<0>( makeBiCGStabSolverWithInfo( tolerance ) );
}

std::vector<double> gmres( const AbsSparseMatrix& A,
                           const std::vector<double>& rhs,
                           std::vector<double>& solution,
                           size_t max_iterations,
                           double threshold )
{
    auto multiplyA = [&]( const double* vector, double* target ) -> void
    {
        A.multiply( vector, target );
    };

    return gmres( multiplyA, &rhs[0], &solution[0], A.size1( ), max_iterations, threshold );
}

std::vector<double> todense( const UnsymmetricSparseMatrix& matrix )
{
    std::vector<double> data( matrix.size1( ) * matrix.size2( ), 0.0 );

    const auto* MLHP_RESTRICT indptr = matrix.indptr( );
    const auto* MLHP_RESTRICT indices = matrix.indices( );
    const auto* MLHP_RESTRICT values = matrix.data( );

    size_t size2 = matrix.size2( );

    for( size_t iRow = 0; iRow < matrix.size1( ); ++iRow )
    {
        for( auto iColumn = indptr[iRow]; iColumn < indptr[iRow + 1]; ++iColumn )
        {
            data[iRow * size2 + indices[iColumn]] = values[iColumn];

        } // iColumn
    } // iRow

    return data;
}

UnsymmetricSparseMatrix filterZeros( const UnsymmetricSparseMatrix& matrix, double tolerance )
{
    SparsePtr newnnz = 0;
    SparsePtr oldnnz = matrix.nnz( );
    SparseIndex nrows = matrix.size2( );

    auto oldindices = matrix.indices( );
    auto oldindptr = matrix.indptr( );
    auto olddata = matrix.data( );

    for( SparsePtr i = 0; i < oldnnz; ++i )
    {
        newnnz = std::abs( olddata[i] ) > tolerance ? newnnz + 1 : newnnz;
    }

    auto newindices = new SparseIndex[newnnz];
    auto newindptr = new SparsePtr[nrows + 1];
    auto newdata = new double[newnnz];

    SparsePtr newindex = 0;

    for( SparseIndex irow = 0; irow < nrows; ++irow )
    {
        newindptr[irow] = newindex;

        for( auto oldindex = oldindptr[irow]; oldindex < oldindptr[irow + 1]; ++oldindex )
        {
            if( std::abs( olddata[oldindex] ) > tolerance )
            {
                newindices[newindex] = oldindices[oldindex];
                newdata[newindex] = olddata[oldindex];

                newindex += 1;
            }
        } // iColumn
    }

    newindptr[nrows] = newindex;

    UnsymmetricSparseMatrix result;

    result.claim( { newindices, newindptr, newdata }, nrows, nrows );

    return result;
}

UnsymmetricSparseMatrix transpose( const UnsymmetricSparseMatrix& matrix )
{
    auto nnz = matrix.nnz( );
    auto size1 = matrix.size1( );
    auto size2 = matrix.size2( );

    auto oldindices = matrix.indices( );
    auto oldindptr = matrix.indptr( );
    auto olddata = matrix.data( );

    auto newindices = new SparseIndex[nnz];
    auto newindptr = new SparsePtr[size2 + 1];
    auto newdata = new double[nnz];

    std::fill( newindptr, newindptr + size2 + 1, 0 );

    for( size_t i = 0; i < nnz; ++i )
    {
        newindptr[oldindices[i] + 1]++;
    }

    std::partial_sum( newindptr, newindptr + size2 + 1, newindptr );

    for( size_t i = 0; i < size1; ++i )
    {
        for( size_t j = oldindptr[i]; j < oldindptr[i + 1]; ++j )
        {
            auto newindex = newindptr[oldindices[j]]++;

            newindices[newindex] = i;
            newdata[newindex] = olddata[j];
        }
    }

    auto previous = SparsePtr { 0 };

    for( size_t i = 0; i < size2 + 1; ++i )
    {
        std::swap( previous, newindptr[i] );
    }

    UnsymmetricSparseMatrix result;

    result.claim( { newindices, newindptr, newdata }, size2, size1 );

    return result;
}

} // mlhp::linalg
