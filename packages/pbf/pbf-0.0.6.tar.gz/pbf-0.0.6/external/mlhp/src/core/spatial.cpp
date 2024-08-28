// This file is part of the mlhp project. License: See LICENSE

#include "mlhp/core/quadrature.hpp"
#include "mlhp/core/spatial.hpp"
#include "mlhp/core/dense.hpp"

#include <string>
#include <sstream>

namespace mlhp::spatial
{

std::array<std::array<double, 3>, 2> findPlaneVectors( std::array<double, 3> normal )
{
    normal = normalize( normal );

    auto min = std::min_element( normal.begin( ), normal.end( ) );
    auto axis = static_cast<size_t>( std::distance( normal.begin( ), min ) );
    auto v1 = spatial::cross( normal, spatial::standardBasisVector<3>( axis ) );

    v1 = spatial::normalize( v1 );

    return { v1, cross( normal, v1 ) };
}

template<size_t D>
MultilinearShapes<D> multilinearShapeFunctions( std::array<double, D> rst, 
                                                std::array<size_t, D> diff )
{
    if( *std::max_element( diff.begin( ), diff.end( ) ) > 1 ) return { };

    auto result = array::make<utilities::binaryPow<size_t>( D )>( 1.0 );

    for( size_t axis = 0; axis < D; ++axis )
    {
        for( size_t i = 0; i < utilities::binaryPow<size_t>( D - 1 ); i += 1 )
        {
            auto ij = nd::binaryUnravel<size_t, D - 1>( i );
            auto i0 = nd::binaryRavel<size_t>( array::insert( ij, axis, size_t { 0 } ) );
            auto i1 = nd::binaryRavel<size_t>( array::insert( ij, axis, size_t { 1 } ) );

            result[i0] *= diff[axis] ? -0.5 : 0.5 * ( 1.0 - rst[axis] );
            result[i1] *= diff[axis] ?  0.5 : 0.5 * ( 1.0 + rst[axis] );
        }
    }

    return result;
}

template<size_t L, size_t G>
JacobianMatrix<G, L> multilinearJacobian( MultilinearCornersSpan<L, G> corners, 
                                          std::array<double, L> rst )
{
    auto J = JacobianMatrix<G, L> { };

    for( size_t axis2 = 0; axis2 < L; ++axis2 )
    {
        auto diff = array::setEntry<size_t, L>( { }, axis2, 1 );
        auto dN = spatial::multilinearShapeFunctions( rst, diff );

        for( size_t i = 0; i < dN.size( ); ++i )
        {
            for( size_t axis1 = 0; axis1 < G; ++axis1 )
            {
                J[axis1 * L + axis2] += dN[i] * corners[i][axis1];
            }
        }
    }

    return J;
}

template<size_t D> MLHP_EXPORT MLHP_PURE
std::array<double, D + 1> simplexShapeFunctions( std::array<double, D> rst, 
                                                 std::array<size_t, D> diff )
{
    auto result = std::array<double, D + 1> { };
    auto ndiff = size_t { 0 }, diffaxis = size_t { 0 };

    for( size_t axis = 0; axis < D; ++axis )
    {
        ndiff += diff[axis];
        diffaxis = diff[axis] ? axis : diffaxis;
    }
    
    if( ndiff == 0 )
    {
        result[0] = 1.0;

        for( size_t axis = 0; axis < D; ++axis )
        {
            result[0] -= rst[axis];
            result[axis + 1] = rst[axis];
        }
    }
    if( ndiff == 1 )
    {
        result[0] = -1;
        result[diffaxis + 1] = 1;
    }

    return result;
}

namespace 
{

// Loosly following https://codereview.stackexchange.com/q/131852
template<bool Side, size_t D>
size_t intersectWithPlane( CoordinateSpan<D> vertices, 
                           size_t nvertices, 
                           size_t axis, 
                           double position ) 
{
    if( nvertices < 2 ) 
    {
        return 0;
    }

    auto classify = [&]( size_t index )
    {
        auto distance = Side ? vertices[index][axis] - position : position - vertices[index][axis];

        return std::pair { vertices[index], distance > 1e-10 ? 1 : ( distance < -1e-10 ? -1 : 0 ) };   
    };

    auto size = vertices.size( ) - 1;
    auto tmp = [&]( size_t index ) -> auto& { return vertices[size - index]; };

    auto [vertexI, classifyI] = classify( 0 );

    auto index = size_t { 0 };
    auto inplane = true;

    for( size_t ivertex = 0; ivertex < nvertices; ++ivertex )
    {
        auto [vertexJ, classifyJ] = classify( nvertices - 1 - ivertex );

        if( classifyJ != 0 )
        {
            if( classifyI == 0 )
            {
                if( index == 0 || tmp( index - 1 ) != vertexI )
                {
                    tmp( index++ ) = vertexI;
                }
            }
            else if( classifyJ != classifyI )
            {
                auto t = ( vertexJ[axis] - position ) / ( vertexJ[axis] - vertexI[axis] );

                tmp( index++ ) = interpolate( vertexJ, vertexI, t );
            }

            if( classifyJ > 0 )
            {
                tmp( index++ ) = vertexJ;
            }

            inplane = false;
        }
        else if( classifyI != 0 )
        {
            tmp( index++ ) = vertexJ;
        }

        vertexI = vertexJ;
        classifyI = classifyJ;
    }

    if( !inplane )
    {
        nvertices = index;

        for( size_t ivertex = 0; ivertex < index; ++ivertex )
        {
            vertices[ivertex] = tmp( index - 1 - ivertex );
        }
    }

    return nvertices;
}

} // namespace

template<size_t D>
CoordinateSpan<D> clipPolygon( CoordinateConstSpan<D> polygon,
                               CoordinateSpan<D> target,
                               size_t axis, double position, bool side )
{
    size_t nvertices = polygon.size( );

    if( target.size( ) != 2 * nvertices )
    {
        MLHP_CHECK( target.size( ) > 2 * nvertices, "Target size in "
                    "clipPolygon needs to be two times the polygon size." );

        target = target.subspan( 0, 2 * nvertices );
    }

    if( polygon.data( ) != target.data( ) )
    {
        std::copy( polygon.begin( ), polygon.end( ), target.rend( ) - utilities::ptrdiff( nvertices ) );
    }
    else
    {
        std::reverse( target.begin( ), target.begin( ) + utilities::ptrdiff( nvertices ) );
    }

    if( side )
    {
        nvertices = intersectWithPlane<true>( target, nvertices, axis, position );
    }
    else
    {
        nvertices = intersectWithPlane<false>( target, nvertices, axis, position );
    }

    auto result = target.subspan( 0, nvertices );

    std::reverse( result.begin( ), result.end( ) );

    return result;
}

template<size_t D>
CoordinateSpan<D> clipPolygon( CoordinateConstSpan<D> polygon, 
                               CoordinateSpan<D> target, 
                               const BoundingBox<D>& bounds )
{
    size_t nvertices = polygon.size( );

    if( target.size( ) != 3 * nvertices )
    {
        MLHP_CHECK( target.size( ) > 3 * nvertices, "Target size in "
                    "clipPolygon needs to be three times the polygon size." );

        target = target.subspan( 0, 3 * nvertices );
    }

    if( polygon.data( ) != target.data( ) )
    {
        std::copy( polygon.begin( ), polygon.end( ), target.rend( ) - utilities::ptrdiff( nvertices ) );
    }
    else
    {
        std::reverse( target.begin( ), target.begin( ) + utilities::ptrdiff( nvertices ) );
    }

    for( size_t axis = 0; axis < D; ++axis ) 
    {
        nvertices = intersectWithPlane<true>( target, nvertices, axis, bounds[0][axis] );
        nvertices = intersectWithPlane<false>( target, nvertices, axis, bounds[1][axis] );
    }

    auto result = target.subspan( 0, nvertices );

    std::reverse( result.begin( ), result.end( ) );

    return result;
}

namespace detail
{

template<size_t D>
double& access( HomogeneousTransformationMatrix<D>& matrix, size_t i, size_t j )
{
    return matrix[i * ( D + 1 ) + j];
}

template<size_t D>
auto scalingMatrix( std::array<double, D> factors )
{
    HomogeneousTransformationMatrix<D> matrix { };

    for( size_t axis = 0; axis < D; ++axis )
    {
        access<D>( matrix, axis, axis ) = factors[axis];
    }

    access<D>( matrix, D, D ) = 1.0;

    return matrix;
}

template<size_t D>
auto translationMatrix( std::array<double, D> vector )
{
    // Start with identity
    auto matrix = scalingMatrix( array::make<D>( 1.0 ) );

    for( size_t axis = 0; axis < D; ++axis )
    {
        access<D>( matrix, axis, D ) = vector[axis];
    }

    return matrix;
}

// https://analyticphysics.com/Higher%20Dimensions/Rotations%20in%20Higher%20Dimensions.htm
template<size_t D>
auto rotationMatrix( std::array<double, D> n1, 
                     std::array<double, D> n2, 
                     double phi )
{
    MLHP_CHECK( std::abs( dot( n1, n1 ) - 1.0 ) < 1e-12 &&
                std::abs( dot( n1, n2 ) ) < 1e-12 &&
                std::abs( dot( n2, n2 ) - 1.0 ) < 1e-12,
                "Implement Gram-Schmidt." );

    // Start with identity
    auto matrix = scalingMatrix( array::make<D>( 1.0 ) );

    double sinPhi = std::sin( phi );
    double cosPhi = std::cos( phi ) - 1.0;

    for( size_t i = 0; i < D; ++i )
    {
        for( size_t j = 0; j < D; ++j )
        {
            double f1 = sinPhi * ( n2[i] * n1[j] - n1[i] * n2[j] );
            double f2 = cosPhi * ( n1[i] * n1[j] + n2[i] * n2[j] );

            access<D>( matrix, i, j ) += f1 + f2;
        }
    }

    return matrix;
}

auto rotationMatrix2D( double phi )
{
    return rotationMatrix<2>( { 1.0, 0.0 }, { 0.0, 1.0 }, phi );
}

auto rotationMatrix3D( std::array<double, 3> axis, double phi )
{
    auto [n1, n2] = findPlaneVectors( axis );

    return rotationMatrix( n1, n2, phi );
}

template<size_t D>
auto concatenate( const auto& matrix1, const auto& matrix2 )
{
    HomogeneousTransformationMatrix<D> target;

    linalg::mmproduct( matrix2.data( ), matrix1.data( ), target.data( ), D + 1 );

    return target;
}

} // namespace detail

template<size_t D> MLHP_EXPORT
HomogeneousTransformation<D> concatenate( const HomogeneousTransformation<D>& transformation1,
                                          const HomogeneousTransformation<D>& transformation2 )
{
    return HomogeneousTransformation<D>{ detail::concatenate<D>( transformation1.matrix, transformation2.matrix ) };
}


template<typename Derived, size_t D>
Derived& HomogeneousTransformationBase<Derived, D>::translate( std::array<double, D> vector )
{
    matrix = detail::concatenate<D>( matrix, detail::translationMatrix( vector ) );

    return static_cast<Derived&>( *this );
}

template<typename Derived, size_t D>
Derived& HomogeneousTransformationBase<Derived, D>::scale( std::array<double, D> factors )
{
    matrix = detail::concatenate<D>( matrix, detail::scalingMatrix( factors ) );

    return static_cast<Derived&>( *this );
}

template<typename Derived, size_t D>
Derived& HomogeneousTransformationBase<Derived, D>::rotate( std::array<double, D> n1, 
                                                            std::array<double, D> n2, 
                                                            double phi )
{
    matrix = detail::concatenate<D>( matrix, detail::rotationMatrix( n1, n2, phi ) );

    return static_cast<Derived&>( *this );
}

template<typename Derived, size_t D>
Derived& HomogeneousTransformationBase<Derived, D>::invert( )
{
    auto source = matrix;

    linalg::invert( source.data( ), matrix.data( ), D + 1 );

    return static_cast<Derived&>( *this );
}

HomogeneousTransformation<2>& HomogeneousTransformation<2>::rotate( double phi )
{
    matrix = detail::concatenate<2>( detail::rotationMatrix2D( phi ), matrix );

    return *this;
}

HomogeneousTransformation<3>& HomogeneousTransformation<3>::rotate( std::array<double, 3> axis, double phi )
{
    matrix = detail::concatenate<3>( matrix, detail::rotationMatrix3D( axis, phi ) );

    return *this;
}

template<size_t D>
HomogeneousTransformation<D> translate( std::array<double, D> vector )
{
    return HomogeneousTransformation<D> { detail::translationMatrix( vector ) };
}

template<size_t D>
HomogeneousTransformation<D> scale( std::array<double, D> factors )
{
    return HomogeneousTransformation<D> { detail::scalingMatrix( factors ) };
}

HomogeneousTransformation<2> rotate( double phi )
{
    return HomogeneousTransformation<2> { detail::rotationMatrix2D( phi ) };
}

HomogeneousTransformation<3> rotate( std::array<double, 3> normal,
                                     double phi )
{
    return HomogeneousTransformation<3> { detail::rotationMatrix3D( normal, phi ) };
}

template<size_t D>
HomogeneousTransformation<D> rotate( std::array<double, D> v1,
                                     std::array<double, D> v2,
                                     double phi )
{
    return HomogeneousTransformation<D> { detail::rotationMatrix( v1, v2, phi ) };
}


template<size_t D> 
void cartesianTickVectors( std::array<size_t, D> ncells,
                           std::array<double, D> lengths,
                           std::array<double, D> origin,
                           CoordinateGrid<D>& target )
{
    for( size_t axis = 0; axis < D; ++axis )
    {
        MLHP_CHECK( ncells[axis] != 0, "Zero number of elements." );

        target[axis].resize( ncells[axis] + 1 );

        for( size_t i = 0; i < ncells[axis] + 1; ++i )
        {
            target[axis][i] = static_cast<double>( i ) / ncells[axis] * lengths[axis] + origin[axis];
        }
    }
}

template<size_t D>
void distributeSeedPoints( CellType type, 
                           size_t nseedpoints, 
                           CoordinateList<D>& rst )
{
    auto size = rst.size( );
    auto limits = array::make<D>( nseedpoints );

    if( type == CellType::NCube )
    {
        auto generator = makeRstGenerator( limits );

        rst.resize( size + array::product( limits ) );

        nd::executeWithIndex( limits, [&]( auto ijk, auto index )
        {
            rst[size + index] = generator( ijk );
        } );
    }
    else
    {
        MLHP_CHECK( type == CellType::Simplex, "Seed grid not implemented for cell type." );
            
        if( nseedpoints == 1 )
        {
            rst.push_back( array::make<D>( 1.0 / ( D + 1.0 ) ) );
        }
        else
        {
            auto origin = array::make<D>( 0.0 );
            auto lengths = array::make<D>( 1.0 );
            auto data = detail::prepareGridIncrements( limits, lengths, origin );

            nd::executeTriangular<D>( nseedpoints, [&]( auto ijk )
            {
                auto dr = std::get<1>( data ) * array::convert<double>( ijk );

                rst.push_back( std::get<0>( data ) + dr );
            } );
        }
    }
}

template<> MLHP_EXPORT
void distributeSeedPoints( CellType, size_t, CoordinateList<0>& rst )
{
    rst.push_back( std::array<double, 0> { } );
}

template<size_t D>
ScalarFunction<D> mask( const ScalarFunction<D>& function,
                        const ImplicitFunction<D>& mask )
{
    return [=]( std::array<double, D> xyz )
    {
        return mask( xyz ) ? function( xyz ) : 0;
    };
}

template<size_t D>
CoordinateGrid<D> cartesianTickVectors( std::array<size_t, D> ncells,
                                        std::array<double, D> lengths,
                                        std::array<double, D> origin )
{
    CoordinateGrid<D> target;

    cartesianTickVectors( ncells, lengths, origin, target );

    return target;
}

template<size_t D>
BoundingBox<D> boundingBox( CoordinateConstSpan<D> coordinates )
{
    auto global = makeEmptyBoundingBox<D>( );

    if( coordinates.size( ) < 4096 )
    { 
        for( auto xyz : coordinates )
        {
            global = boundingBoxOr( global, xyz );
        }
    }
    else
    {
        #pragma omp parallel
        {
            auto local = makeEmptyBoundingBox<D>( );
            auto nvertices = static_cast<std::int64_t>( coordinates.size( ) );

            #pragma omp parallel for schedule( dynamic, 4096 )
            for( std::int64_t ii = 0; ii < nvertices; ++ii )
            {
                local = boundingBoxOr( local, coordinates[static_cast<size_t>( ii )] );
            }

            #pragma omp critical
            {
                global = boundingBoxOr( global, local );
            }
        }
    }

    return global;
}

template<size_t D>
ScalarFunction<D> voxelFunction( const std::vector<double>& data,
                                 std::array<size_t, D> nvoxels,
                                 std::array<double, D> lengths,
                                 std::array<double, D> origin,
                                 std::optional<double> outside )
{
    auto size = array::product( nvoxels );

    MLHP_CHECK( data.size( ) == size, "Inconsistent voxel grid and data sizes." );
    MLHP_CHECK( size != 0, "Zero voxels given." );

    if( outside )
    {
        return [=]( std::array<double, D> xyz )
        { 
            auto index = findVoxel( nvoxels, lengths, origin, xyz );

            return index ? data[*index] : *outside;
        };
    }
    else
    {
        return [=]( std::array<double, D> xyz )
        { 
            auto index = findVoxel( nvoxels, lengths, origin, xyz );

            MLHP_CHECK( index, "No voxel at given position and no outside value specified." );

            return data[*index];
        };
    }
}

template<size_t D>
spatial::ScalarFunction<D> extractComponent( const spatial::VectorFunction<D>& function, size_t icomponent )
{
    MLHP_CHECK( icomponent < function.odim, "Invalid component index." );

    auto cache = std::make_shared<utilities::ThreadLocalContainer<std::vector<double>>>( );

    for( auto& vec : cache->data )
    {
        vec.resize( function.odim );
    }

    return [=]( std::array<double, D> xyz )
    {
        auto& vec = cache->get( );

        function( xyz, vec );

        return vec[icomponent];
    };
}

template<size_t D>
CoordinateList<D> tensorProduct( const CoordinateGrid<D>& grid )
{
    auto result = CoordinateList<D>{ };

    tensorProduct( grid, result );

    return result;
}

template<size_t D>
void tensorProduct( const CoordinateGrid<D>& grid, 
                    CoordinateList<D>& target )
{
    auto offset = target.size( );
    auto sizes = array::elementSizes( grid );

    target.resize( offset + array::product( sizes ) );

    nd::executeWithIndex( sizes, [&]( std::array<size_t, D> ijk, size_t index )
    {
        target[offset + index] = array::extract( grid, ijk );
    } );
}

template<size_t D> 
std::optional<std::uint64_t> findVoxel( std::array<size_t, D> nvoxels, 
                                        std::array<double, D> lengths,
                                        std::array<double, D> origin,
                                        std::array<double, D> xyz )
{
    auto findVoxel1D = []( size_t n, double x0, double dx, double x ) -> std::optional<std::uint64_t>
    {
        MLHP_CHECK( n != 0, "Zero number of voxels." );

        auto r = (x - x0) / dx * n;

        if( r > 0.0 && r < n )
        {
            return static_cast<std::uint64_t>( r );
        }
        else if( std::abs( r ) < 1e-10 )
        {
            return std::uint64_t { 0 };
        }
        else if( std::abs( r - n ) < 1e-10 )
        {
            return std::uint64_t { n - 1 };
        }
        
        return std::nullopt;
    };

    auto stride = std::uint64_t { 1 };
    auto index = std::uint64_t { 0 };

    for( size_t axis = 0; axis < D; ++axis )
    {
        auto a = D - axis - 1;
        auto i = findVoxel1D( nvoxels[a], origin[a], lengths[a], xyz[a] );

        if( !i ) return std::nullopt;

        index += stride * (*i);
        stride *= nvoxels[a];
    }

    return index;
}

// https://stackoverflow.com/a/26127012
void fibonacciSphere( CoordinateSpan<3> target )
{
    auto npoints = target.size( );
    auto phi = std::numbers::pi * ( std::sqrt( 5.0 ) - 1.0 );

    for( size_t i = 0; i < npoints; ++i )
    {
        auto y = 1.0 - 2.0 * i / ( npoints - 1.0 );
        auto r = std::sqrt( 1.0 - y * y );
        auto theta = phi * i;

        target[i] = { r * std::cos( theta ), y, r * std::sin( theta ) };
    }
}

CoordinateList<3> fibonacciSphere( size_t n )
{
    auto target = CoordinateList<3>( n );

    fibonacciSphere( target );

    return target;
}

#define MLHP_INSTANTIATE_DIM( D )                                                              \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    CoordinateSpan<D> clipPolygon( CoordinateConstSpan<D> polygon,                             \
                                   CoordinateSpan<D> target,                                   \
                                   size_t axis, double position, bool side );                  \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    CoordinateSpan<D> clipPolygon( CoordinateConstSpan<D> polygon,                             \
                                CoordinateSpan<D> target,                                      \
                                const BoundingBox<D>& bounds );                                \
                                                                                               \
    template struct MLHP_EXPORT HomogeneousTransformation<D>;                                  \
    template struct MLHP_EXPORT HomogeneousTransformationBase<HomogeneousTransformation<D>,D>; \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    HomogeneousTransformation<D> translate( std::array<double, D> vector );                    \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    HomogeneousTransformation<D> scale( std::array<double, D> factors );                       \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    HomogeneousTransformation<D> rotate( std::array<double, D> v1,                             \
                                         std::array<double, D> v2,                             \
                                         double phi );                                         \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    HomogeneousTransformation<D> concatenate( const HomogeneousTransformation<D>& t1,          \
                                              const HomogeneousTransformation<D>& t2 );        \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    ScalarFunction<D> mask( const ScalarFunction<D>& function,                                 \
                            const ImplicitFunction<D>& mask );                                 \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    void cartesianTickVectors( std::array<size_t, D> ncells,                                   \
                               std::array<double, D> lengths,                                  \
                               std::array<double, D> origin,                                   \
                               CoordinateGrid<D>& target );                                    \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    CoordinateGrid<D> cartesianTickVectors( std::array<size_t, D> ncells,                      \
                                            std::array<double, D> lengths,                     \
                                            std::array<double, D> origin );                    \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    void distributeSeedPoints( CellType type,                                                  \
                               size_t nseedpoints,                                             \
                               CoordinateList<D>& rst );                                       \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    BoundingBox<D> boundingBox( CoordinateConstSpan<D> coordinates );                          \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    ScalarFunction<D> extractComponent( const VectorFunction<D>& function, size_t icomponent );\
                                                                                               \
    template MLHP_EXPORT                                                                       \
    CoordinateList<D> tensorProduct( const CoordinateGrid<D>& grid );                          \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    void tensorProduct( const CoordinateGrid<D>& grid,                                         \
                        CoordinateList<D>& target );                                           \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    std::optional<std::uint64_t> findVoxel( std::array<size_t, D> nvoxels,                     \
                                            std::array<double, D> lengths,                     \
                                            std::array<double, D> origin,                      \
                                            std::array<double, D> xyz );                       \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    ScalarFunction<D> voxelFunction( const std::vector<double>& data,                          \
                                     std::array<size_t, D> nvoxels,                            \
                                     std::array<double, D> lengths,                            \
                                     std::array<double, D> origin,                             \
                                     std::optional<double> outside );                          \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    MultilinearShapes<D> multilinearShapeFunctions<D>( std::array<double, D> rst,              \
                                                       std::array<size_t, D> diff );           \
                                                                                               \
    template MLHP_EXPORT MLHP_PURE                                                             \
    std::array<double, D + 1> simplexShapeFunctions( std::array<double, D> rst,                \
                                                     std::array<size_t, D> diff );             \
                                                                                               \
    template MLHP_EXPORT                                                                       \
    JacobianMatrix<D, D> multilinearJacobian( MultilinearCornersSpan<D, D> corners,            \
                                              std::array<double, D> rst);

MLHP_DIMENSIONS_XMACRO_LIST
#undef MLHP_INSTANTIATE_DIM

} // namespace mlhp::spatial

namespace mlhp::solution
{

template<size_t D>
spatial::ScalarFunction<D + 1> amLinearHeatSource( const spatial::ParameterFunction<D>& path,
                                                   const RealFunction& intensity,
                                                   double sigma )
{
    auto function = spatial::integralNormalizedGaussBell<D>( std::array<double, D>{ }, sigma, 1.0 );

    return spatial::revolveAroundPath<D>( function, path, intensity );
}

template<size_t D>
spatial::ScalarFunction<D + 1> amLinearHeatSolution( const spatial::ParameterFunction<D>& path,
                                                     const RealFunction& intensity,
                                                     double capacity, double kappa,
                                                     double sigma, double dt, double shift )
{
    double sigma2 = 2.0 * sigma * sigma;
    double kappaCapacity = 4.0 * kappa / capacity;
    double scaling = 1.0 / ( capacity * utilities::integerPow( std::sqrt( std::numbers::pi ), D ) );

    auto Gf = [=]( std::array<double, D + 1> xyt )
    {
        double r2 = 0.0;

        for( size_t axis = 0; axis < D; ++axis )
        {
            r2 += xyt[axis] * xyt[axis];
        }

        double invWSquared = 1.0 / ( sigma2 + kappaCapacity * xyt[D] );

        return scaling * utilities::integerPow( std::sqrt( invWSquared ), D ) * std::exp( -r2 * invWSquared );
    };

    auto points = gaussLegendrePoints( 30 );

    auto integrateInterval = [=]( double t0, double t1, const auto& function )
    {
        double value = 0.0;

        for( size_t i = 0; i < points[0].size( ); ++i )
        {
            double coordinate = 0.5 * ( points[0][i] + 1 ) * ( t1 - t0 ) + t0;
            double weight = ( t1 - t0 ) / 2.0 * points[1][i];

            value += function( coordinate ) * weight;
        }

        return value;
    };

    auto integrator = [=]( std::array<double, D + 1> xyt )
    {
        auto n = static_cast<size_t>( std::ceil( xyt[D] / dt ) );
        double step = xyt[D] / n;

        double value = 0.0;

        auto integrand = [=]( double tau )
        {
            auto asdf = array::insert( path( tau ), D, tau );

            return Gf( array::subtract( xyt, asdf ) ) * intensity( tau );
        };

        for( size_t i = 0; i < n; ++i )
        {
            value += integrateInterval( step * i, step * (i + 1), integrand );
        }

        return value + shift;
    };

    return integrator;
}

template<size_t D>
spatial::ScalarFunction<D> singularSolution( )
{
    return []( std::array<double, D> xyz )
    {
        return std::pow( spatial::normSquared( xyz ), 1.0 / 4.0 );
    };
}

template<> MLHP_EXPORT
spatial::ScalarFunction<1> singularSolution( )
{
    return []( std::array<double, 1> x ) noexcept
    {
        double gamma = 0.65;

        return std::pow( x[0], gamma ) - gamma * x[0];
    };
}

template<size_t D>
spatial::VectorFunction<D, D> singularSolutionDerivatives( )
{
    return [=]( std::array<double, D> xyz )
    {
        return array::multiply( xyz, 0.5 / std::pow( spatial::normSquared( xyz ), 3.0 / 4.0 ) );
    };
}

template<> MLHP_EXPORT
spatial::VectorFunction<1, 1> singularSolutionDerivatives( )
{
    return []( std::array<double, 1> x ) noexcept
    {
        double gamma = 0.65;

        return std::array { gamma * std::pow( x[0], gamma - 1.0 ) - gamma };
    };
}

template<size_t D>
spatial::ScalarFunction<D> singularSolutionSource( )
{
    return []( std::array<double, D> xyz )
    {
        return ( 3.0 - 2.0 * D ) / 4.0 * std::pow( spatial::normSquared( xyz ), -3.0 / 4.0 );
    };
}

template<> MLHP_EXPORT
spatial::ScalarFunction<1> singularSolutionSource( )
{
    return []( std::array<double, 1> x ) noexcept
    {
        double gamma = 0.65;

        return -gamma * ( gamma - 1.0 ) * std::pow( x[0], gamma - 2.0 );
    };
}

#define MLHP_INSTANTIATE_DIM( D )                                                                   \
    template MLHP_EXPORT                                                                            \
    spatial::ScalarFunction<D + 1> amLinearHeatSource( const spatial::ParameterFunction<D>& path,   \
                                                       const RealFunction& intensity,               \
                                                       double sigma );                              \
                                                                                                    \
    template MLHP_EXPORT                                                                            \
    spatial::ScalarFunction<D + 1> amLinearHeatSolution( const spatial::ParameterFunction<D>& path, \
                                                         const RealFunction& intensity,             \
                                                         double capacity, double kappa,             \
                                                         double sigma, double dt,                   \
                                                         double shift );                            \
                                                                                                    \
    template MLHP_EXPORT                                                                            \
    spatial::ScalarFunction<D> singularSolution<D>( );                                              \
                                                                                                    \
    template MLHP_EXPORT                                                                            \
    spatial::VectorFunction<D, D> singularSolutionDerivatives<D>( );                                \
                                                                                                    \
    template MLHP_EXPORT                                                                            \
    spatial::ScalarFunction<D> singularSolutionSource<D>( );

    MLHP_DIMENSIONS_XMACRO_LIST
#undef MLHP_INSTANTIATE_DIM

} // namespace mlhp::solution
