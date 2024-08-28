// This file is part of the mlhp project. License: See LICENSE

#ifndef MLHP_CORE_DENSE_IMPL_HPP
#define MLHP_CORE_DENSE_IMPL_HPP

namespace mlhp::linalg
{

template<typename DenseMatrixType> inline
constexpr size_t denseRowIncrement( size_t iRow, size_t paddedLength )
{
    if constexpr( isSymmetricDense<DenseMatrixType> )
    {
        return memory::paddedLength<double>( iRow + 1 );
    }
    else
    {
        return paddedLength;
    }
}

template<typename T> inline
auto symmetricNumberOfBlocks( size_t irow )
{
    constexpr auto simdSize = memory::simdVectorSize<T>( );
    constexpr auto halfSimdSize = simdSize / 2;

    if constexpr( simdSize == 1 )
    {
        return ( irow * ( irow + 1 ) ) / 2;
    }

    auto truncatedI = irow / simdSize;

    return ( irow - truncatedI * halfSimdSize ) * ( truncatedI + 1 );
}

template<typename T> inline
auto symmetricDenseOffset( size_t rowI, size_t columnJ )
{
    constexpr auto simdSize = memory::simdVectorSize<T>( );

    return symmetricNumberOfBlocks<T>( rowI ) * simdSize + columnJ;
}

template<typename MatrixType, typename T> inline
auto indexDenseMatrix( T* matrix, size_t i, size_t j, size_t paddedSize )
{
    if constexpr( linalg::isSymmetricDense<MatrixType> )
    {
        if( j > i )
        {
            return matrix[linalg::symmetricDenseOffset<double>( j, i )];
        }
        else
        {
            return matrix[linalg::symmetricDenseOffset<double>( i, j )];
        }
    }
    else
    {
        return matrix[i * paddedSize + j];
    }
}

template<typename MatrixType, typename T> inline
auto denseMatrixStorageSize( size_t size )
{
    if constexpr( isSymmetricDense<MatrixType> )
    {
        return symmetricNumberOfBlocks<T>( size ) * memory::simdVectorSize<T>( );
    }
    else
    {
        return size * memory::paddedLength<T>( size );
    }
}

template<typename TargetMatrixType, typename MatrixExpr> inline
void elementLhs( double* target, size_t allsize1, 
                 size_t offset0, size_t size0,
                 size_t offset1, size_t size1, 
                 MatrixExpr&& expression )
{
    auto paddedSize = memory::paddedLength<double>( allsize1 );
    auto rowOffset = isUnsymmetricDense<TargetMatrixType> ? offset0 * paddedSize :
        symmetricNumberOfBlocks<double>( offset0 ) * memory::simdVectorSize<double>( );

    auto lhs = memory::assumeAlignedNoalias( target + rowOffset );

    for( size_t irow = 0; irow < size0; ++irow )
    {
        auto rowSize = linalg::denseRowIncrement<TargetMatrixType>( offset0 + irow, paddedSize );

        for( size_t icolumn = 0; offset1 + icolumn < std::min( rowSize, offset1 + size1 ); ++icolumn )
        {
            lhs[offset1 + icolumn] += expression( irow, icolumn );
        }
        
        lhs += rowSize;
    }
}

template<typename TargetMatrixType, typename MatrixExpr> inline
void elementLhs( double* target, size_t size, size_t nblocks, MatrixExpr&& expression )
{
    auto lhs = memory::assumeAlignedNoalias( target );
    
    constexpr auto blocksize = memory::simdVectorSize<double>( );

    size_t paddedSize = nblocks * blocksize;

    //for( size_t iRow = 0; iRow < size; ++iRow )
    //{
    //    auto rowSize = linalg::denseRowIncrement<TargetMatrixType>( iRow, paddedSize );
    //
    //    for( size_t iColumn = 0; iColumn < rowSize; ++iColumn )
    //    {
    //        lhs[iColumn] += function( iRow, iColumn );
    //        
    //    } // iColumn
    //    
    //    lhs += rowSize;
    //    
    //} // iRow

    auto writeRow = [&]( size_t iRow, size_t rowSize )
    {
        for( size_t iColumn = 0; iColumn < rowSize; ++iColumn )
        {
            lhs[iColumn] += expression( iRow, iColumn );
        }

        lhs += rowSize;
    };

    if constexpr( isUnsymmetricDense<TargetMatrixType> )
    {
        for( size_t iRow = 0; iRow < size; ++iRow )
        {
            writeRow( iRow, paddedSize );

        } // iRow
    }
    else
    {
        // Write blocks of rows
        for( size_t iBlock = 0; iBlock + 1 < nblocks; ++iBlock )
        {
            size_t rowSize = ( iBlock + 1 ) * blocksize;

            for( size_t iBlockRow = 0; iBlockRow < blocksize; ++iBlockRow )
            {
                writeRow( iBlock * blocksize + iBlockRow, rowSize );
            }
        }

        // Peel remaining rows
        for( size_t iPeeledRow = 0; iPeeledRow < size - ( nblocks - 1 ) * blocksize; ++iPeeledRow )
        {
            writeRow( iPeeledRow + ( nblocks - 1 ) * blocksize, paddedSize );
        }
    }
}

template<typename MatrixExpr> inline
void symmetricElementLhs( double* target, size_t size, size_t nblocks, MatrixExpr&& expression )
{
    elementLhs<linalg::SymmetricDenseMatrix>( target, size, nblocks, std::forward<MatrixExpr>( expression ) );
}

template<typename MatrixExpr> inline
void unsymmetricElementLhs( double* target, size_t size, size_t nblocks, MatrixExpr&& expression )
{
    elementLhs<linalg::UnsymmetricDenseMatrix>( target, size, nblocks, std::forward<MatrixExpr>( expression ) );
}

template<typename VectorExpr> inline
void elementRhs( double* target, size_t size, size_t, VectorExpr&& expression )
{
    // Not aligned, not padded, for multiple field components
    auto rhs = memory::assumeNoalias( target );
    
    for( size_t iRow = 0; iRow < size; ++iRow )
    {
        rhs[iRow] += expression( iRow );
    }
}

namespace detail
{

template<typename T, size_t Extent>
inline auto adapter( std::span<T, Extent> span, size_t size1 )
{
    return [=]( size_t i, size_t j ) -> T&
    {
        return span[i * size1 + j];
    };
}

} // detail

template<typename T> inline
auto adapter( T&& span, size_t size1 )
{
    return detail::adapter( std::span( span ), size1 );
}

inline void mmproduct( const double* left, const double* right, double* target, size_t leftM, size_t leftN, size_t rightN )
{
    auto L = memory::assumeNoalias( left );
    auto R = memory::assumeNoalias( right );
    auto T = memory::assumeNoalias( target );

    for( size_t i = 0; i < leftM; ++i )
    {
        for( size_t j = 0; j < rightN; ++j )
        {
            T[i * rightN + j] = 0.0;

            for( size_t k = 0; k < leftN; ++k )
            {
                T[i * rightN + j] += L[i * leftN + k] * R[k * rightN + j];
            }
        }
    }
}

inline void mmproduct( const double* left, const double* right, double* target, size_t size )
{
    mmproduct( left, right, target, size, size, size );
}

inline void mvproduct( const double* M, const double* v, double* target, size_t size1, size_t size2 )
{
    for( size_t i = 0; i < size1; ++i )
    {
        for( size_t j = 0; j < size2; ++j )
        {
            target[i] += M[i * size2 + j] * v[j];
        }
    }
}

inline void mvproduct( const double* M, const double* v, double* target, size_t size )
{
    mvproduct( M, v, target, size, size );
}

template<size_t D1, size_t D2> inline
std::array<double, D1> mvproduct( const double* M, std::array<double, D2> v )
{
    auto target = std::array<double, D1> { };

    mvproduct( M, v.data( ), target.data( ), D1, D2 );

    return target;
}

template<size_t D> inline
std::array<double, D> mvproduct( const double* M, std::array<double, D> v )
{
    return mvproduct<D, D>( M, v );
}

template<size_t D1, size_t D2> inline
std::array<double, D1> mvproduct( const std::array<double, D1 * D2>& M, std::array<double, D2> v )
{
    return mvproduct<D1, D2>( M.data( ), v );
}


} // namespace mlhp::linalg

#endif // MLHP_CORE_DENSE_IMPL_HPP
