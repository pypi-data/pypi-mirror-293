// This file is part of the mlhp project. License: See LICENSE

#include "mlhp/core/dense.hpp"
#include "mlhp/core/utilities.hpp"

namespace mlhp::linalg
{

void lu( double* M, size_t* p, size_t size )
{
    std::iota( p, p + size, size_t { 0 } );

    for( size_t i = 0; i < size; ++i )
    {
        double* MLHP_RESTRICT rowI = M + i * size;

        size_t pivot = i;

        // First find index of largest value in column below (i, i)
        for( size_t j = i + 1; j < size; ++j )
        {
            pivot = std::abs( M[pivot * size + i] ) >
                    std::abs( M[j * size + i] ) ? pivot : j;
        }

        // Swap rows i and pivot
        if( i != pivot )
        { 
            std::swap( p[i], p[pivot] );
            std::swap_ranges( rowI, rowI + size, M + pivot * size );
        }

        // Then loop over all rows below and subtract row i accordingly
        for( size_t j = i + 1; j < size; ++j )
        {
            auto* MLHP_RESTRICT rowJ = M + j * size;

            rowJ[i] /= rowI[i];

            for( size_t k = i + 1; k < size; ++k )
            {
                rowJ[k] -= rowJ[i] * rowI[k];

            } // for k
        } // for j
    } // for j
}

void luSubstitute( const double* LU, const size_t* p, size_t size, const double* b, double* u )
{
    // Initialize u from permuting b
    for( size_t i = 0; i < size; ++i )
    {
        u[i] = b[p[i]];
    }

    // Forward substitution
    for( size_t i = 1; i < size; ++i )
    {
        const double* MLHP_RESTRICT rowI = LU + i * size;

        for( size_t j = 0; j < i; ++j )
        {
            u[i] -= rowI[j] * u[j];
        }
    }

    // Backward substitution
    for( size_t r = 0; r < size; ++r )
    {
        size_t i = size - 1 - r;

        const double* MLHP_RESTRICT rowI = LU + i * size;

        for( size_t j = i + 1; j < size; ++j )
        {
            u[i] -= rowI[j] * u[j];
        }

        u[i] /= rowI[i];
    }
}

void luInvert( double* LU, size_t* p, size_t size, double* I )
{
    // Initialize permuted identity matrix
    std::fill( I, I + size * size, 0.0 );

    for( size_t i = 0; i < size; ++i )
    {
        I[i * size + p[i]] = 1.0;
    }

     // Forward substitution
    for( size_t i = 1; i < size; ++i )
    {
        const double* MLHP_RESTRICT luRowI = LU + i * size;

        for( size_t j = 0; j < i; ++j )
        {
            double* MLHP_RESTRICT invRowI = I + i * size;
            double* MLHP_RESTRICT invRowJ = I + j * size;

            for( size_t k = 0; k < size; ++k )
            {
                invRowI[k] -= luRowI[j] * invRowJ[k];
            }

        }
    }

    // Backward substitution
    for( size_t r = 0; r < size; ++r )
    {
        size_t i = size - 1 - r;

        const double* MLHP_RESTRICT luRowI = LU + i * size;

        for( size_t j = i + 1; j < size; ++j )
        {
            double* MLHP_RESTRICT invRowI = I + i * size;
            double* MLHP_RESTRICT invRowJ = I + j * size;

            for( size_t k = 0; k < size; ++k )
            {
                invRowI[k] -= luRowI[j] * invRowJ[k];
            }
        }

        for( size_t k = 0; k < size; ++k )
        {
            I[i * size + k] /= luRowI[i];
        }

    } // for r
}

double luDeterminant( const double* LU, size_t size )
{
    double det = 1.0;

    for( size_t i = 0; i < size; ++i )
    {
        det *= LU[i * size + i];
    }

    return std::abs( det );
}

// See also blaze/math/dense/Inversion.h
double invertSmall2( const auto& S, auto& T )
{
    T( 0, 0 ) = S( 1, 1 );
    T( 1, 0 ) = -S( 1, 0 );
    T( 0, 1 ) = -S( 0, 1 );
    T( 1, 1 ) = S( 0, 0 );

    return S( 0, 0 ) * S( 1, 1 ) - S( 0, 1 ) * S( 1, 0 );
}

// See also blaze/math/dense/Inversion.h
double invertSmallUnsymmetric3( const auto& S, auto& T )
{
    T( 0, 0 ) = S( 1, 1 ) * S( 2, 2 ) - S( 1, 2 ) * S( 2, 1 );
    T( 1, 0 ) = S( 1, 2 ) * S( 2, 0 ) - S( 1, 0 ) * S( 2, 2 );
    T( 2, 0 ) = S( 1, 0 ) * S( 2, 1 ) - S( 1, 1 ) * S( 2, 0 );

    double det =( S( 0, 0 ) * T( 0, 0 ) + S( 0, 1 ) * T( 1, 0 ) + S( 0, 2 ) * T( 2, 0 ) );

    T( 0, 1 ) = S( 0, 2 ) * S( 2, 1 ) - S( 0, 1 ) * S( 2, 2 );
    T( 1, 1 ) = S( 0, 0 ) * S( 2, 2 ) - S( 0, 2 ) * S( 2, 0 );
    T( 2, 1 ) = S( 0, 1 ) * S( 2, 0 ) - S( 0, 0 ) * S( 2, 1 );
    T( 0, 2 ) = S( 0, 1 ) * S( 1, 2 ) - S( 0, 2 ) * S( 1, 1 );
    T( 1, 2 ) = S( 0, 2 ) * S( 1, 0 ) - S( 0, 0 ) * S( 1, 2 );
    T( 2, 2 ) = S( 0, 0 ) * S( 1, 1 ) - S( 0, 1 ) * S( 1, 0 );

    return det;
}

// See also blaze/math/dense/Inversion.h
double invertSmallUnsymmetric4( const auto& S, auto& T )
{
    double tmp1 = S( 2, 2 ) * S( 3, 3 ) - S( 2, 3 ) * S( 3, 2 );
    double tmp2 = S( 2, 1 ) * S( 3, 3 ) - S( 2, 3 ) * S( 3, 1 );
    double tmp3 = S( 2, 1 ) * S( 3, 2 ) - S( 2, 2 ) * S( 3, 1 );

    T( 0, 0 ) = S( 1, 1 ) * tmp1 - S( 1, 2 ) * tmp2 + S( 1, 3 ) * tmp3;
    T( 0, 1 ) = S( 0, 2 ) * tmp2 - S( 0, 1 ) * tmp1 - S( 0, 3 ) * tmp3;

    double tmp4 = S( 2, 0 ) * S( 3, 3 ) - S( 2, 3 ) * S( 3, 0 );
    double tmp5 = S( 2, 0 ) * S( 3, 2 ) - S( 2, 2 ) * S( 3, 0 );

    T( 1, 0 ) = S( 1, 2 ) * tmp4 - S( 1, 0 ) * tmp1 - S( 1, 3 ) * tmp5;
    T( 1, 1 ) = S( 0, 0 ) * tmp1 - S( 0, 2 ) * tmp4 + S( 0, 3 ) * tmp5;

    tmp1 = S( 2, 0 ) * S( 3, 1 ) - S( 2, 1 ) * S( 3, 0 );

    T( 2, 0 ) = S( 1, 0 ) * tmp2 - S( 1, 1 ) * tmp4 + S( 1, 3 ) * tmp1;
    T( 2, 1 ) = S( 0, 1 ) * tmp4 - S( 0, 0 ) * tmp2 - S( 0, 3 ) * tmp1;
    T( 3, 0 ) = S( 1, 1 ) * tmp5 - S( 1, 0 ) * tmp3 - S( 1, 2 ) * tmp1;
    T( 3, 1 ) = S( 0, 0 ) * tmp3 - S( 0, 1 ) * tmp5 + S( 0, 2 ) * tmp1;

    tmp1 = S( 0, 2 ) * S( 1, 3 ) - S( 0, 3 ) * S( 1, 2 );
    tmp2 = S( 0, 1 ) * S( 1, 3 ) - S( 0, 3 ) * S( 1, 1 );
    tmp3 = S( 0, 1 ) * S( 1, 2 ) - S( 0, 2 ) * S( 1, 1 );

    T( 0, 2 ) = S( 3, 1 ) * tmp1 - S( 3, 2 ) * tmp2 + S( 3, 3 ) * tmp3;
    T( 0, 3 ) = S( 2, 2 ) * tmp2 - S( 2, 1 ) * tmp1 - S( 2, 3 ) * tmp3;

    tmp4 = S( 0, 0 ) * S( 1, 3 ) - S( 0, 3 ) * S( 1, 0 );
    tmp5 = S( 0, 0 ) * S( 1, 2 ) - S( 0, 2 ) * S( 1, 0 );

    T( 1, 2 ) = S( 3, 2 ) * tmp4 - S( 3, 0 ) * tmp1 - S( 3, 3 ) * tmp5;
    T( 1, 3 ) = S( 2, 0 ) * tmp1 - S( 2, 2 ) * tmp4 + S( 2, 3 ) * tmp5;

    tmp1 = S( 0, 0 ) * S( 1, 1 ) - S( 0, 1 ) * S( 1, 0 );

    T( 2, 2 ) = S( 3, 0 ) * tmp2 - S( 3, 1 ) * tmp4 + S( 3, 3 ) * tmp1;
    T( 2, 3 ) = S( 2, 1 ) * tmp4 - S( 2, 0 ) * tmp2 - S( 2, 3 ) * tmp1;
    T( 3, 2 ) = S( 3, 1 ) * tmp5 - S( 3, 0 ) * tmp3 - S( 3, 2 ) * tmp1;
    T( 3, 3 ) = S( 2, 0 ) * tmp3 - S( 2, 1 ) * tmp5 + S( 2, 2 ) * tmp1;

    return S( 0, 0 ) * T( 0, 0 ) + S( 0, 1 ) * T( 1, 0 ) + 
           S( 0, 2 ) * T( 2, 0 ) + S( 0, 3 ) * T( 3, 0 );
}

// See also blaze/math/dense/Inversion.h
double invertSmallUnsymmetric5( const auto& S, auto& T )
{
    double tmp1 = S( 3, 3 ) * S( 4, 4 ) - S( 3, 4 ) * S( 4, 3 );
    double tmp2 = S( 3, 2 ) * S( 4, 4 ) - S( 3, 4 ) * S( 4, 2 );
    double tmp3 = S( 3, 2 ) * S( 4, 3 ) - S( 3, 3 ) * S( 4, 2 );
    double tmp4 = S( 3, 1 ) * S( 4, 4 ) - S( 3, 4 ) * S( 4, 1 );
    double tmp5 = S( 3, 1 ) * S( 4, 3 ) - S( 3, 3 ) * S( 4, 1 );
    double tmp6 = S( 3, 1 ) * S( 4, 2 ) - S( 3, 2 ) * S( 4, 1 );
    double tmp7 = S( 3, 0 ) * S( 4, 4 ) - S( 3, 4 ) * S( 4, 0 );
    double tmp8 = S( 3, 0 ) * S( 4, 3 ) - S( 3, 3 ) * S( 4, 0 );
    double tmp9 = S( 3, 0 ) * S( 4, 2 ) - S( 3, 2 ) * S( 4, 0 );
    double tmp10 = S( 3, 0 ) * S( 4, 1 ) - S( 3, 1 ) * S( 4, 0 );

    double tmp11 = S( 2, 2 ) * tmp1 - S( 2, 3 ) * tmp2 + S( 2, 4 ) * tmp3;
    double tmp12 = S( 2, 1 ) * tmp1 - S( 2, 3 ) * tmp4 + S( 2, 4 ) * tmp5;
    double tmp13 = S( 2, 1 ) * tmp2 - S( 2, 2 ) * tmp4 + S( 2, 4 ) * tmp6;
    double tmp14 = S( 2, 1 ) * tmp3 - S( 2, 2 ) * tmp5 + S( 2, 3 ) * tmp6;
    double tmp15 = S( 2, 0 ) * tmp1 - S( 2, 3 ) * tmp7 + S( 2, 4 ) * tmp8;
    double tmp16 = S( 2, 0 ) * tmp2 - S( 2, 2 ) * tmp7 + S( 2, 4 ) * tmp9;
    double tmp17 = S( 2, 0 ) * tmp3 - S( 2, 2 ) * tmp8 + S( 2, 3 ) * tmp9;

    T( 0, 0 ) = S( 1, 1 ) * tmp11 - S( 1, 2 ) * tmp12 + S( 1, 3 ) * tmp13 - S( 1, 4 ) * tmp14;
    T( 0, 1 ) = -S( 0, 1 ) * tmp11 + S( 0, 2 ) * tmp12 - S( 0, 3 ) * tmp13 + S( 0, 4 ) * tmp14;
    T( 1, 0 ) = -S( 1, 0 ) * tmp11 + S( 1, 2 ) * tmp15 - S( 1, 3 ) * tmp16 + S( 1, 4 ) * tmp17;
    T( 1, 1 ) = S( 0, 0 ) * tmp11 - S( 0, 2 ) * tmp15 + S( 0, 3 ) * tmp16 - S( 0, 4 ) * tmp17;

    double tmp18 = S( 2, 0 ) * tmp4 - S( 2, 1 ) * tmp7 + S( 2, 4 ) * tmp10;
    double tmp19 = S( 2, 0 ) * tmp5 - S( 2, 1 ) * tmp8 + S( 2, 3 ) * tmp10;
    double tmp20 = S( 2, 0 ) * tmp6 - S( 2, 1 ) * tmp9 + S( 2, 2 ) * tmp10;

    T( 2, 0 ) = S( 1, 0 ) * tmp12 - S( 1, 1 ) * tmp15 + S( 1, 3 ) * tmp18 - S( 1, 4 ) * tmp19;
    T( 2, 1 ) = -S( 0, 0 ) * tmp12 + S( 0, 1 ) * tmp15 - S( 0, 3 ) * tmp18 + S( 0, 4 ) * tmp19;
    T( 3, 0 ) = -S( 1, 0 ) * tmp13 + S( 1, 1 ) * tmp16 - S( 1, 2 ) * tmp18 + S( 1, 4 ) * tmp20;
    T( 3, 1 ) = S( 0, 0 ) * tmp13 - S( 0, 1 ) * tmp16 + S( 0, 2 ) * tmp18 - S( 0, 4 ) * tmp20;
    T( 4, 0 ) = S( 1, 0 ) * tmp14 - S( 1, 1 ) * tmp17 + S( 1, 2 ) * tmp19 - S( 1, 3 ) * tmp20;
    T( 4, 1 ) = -S( 0, 0 ) * tmp14 + S( 0, 1 ) * tmp17 - S( 0, 2 ) * tmp19 + S( 0, 3 ) * tmp20;

    tmp11 = S( 1, 2 ) * tmp1 - S( 1, 3 ) * tmp2 + S( 1, 4 ) * tmp3;
    tmp12 = S( 1, 1 ) * tmp1 - S( 1, 3 ) * tmp4 + S( 1, 4 ) * tmp5;
    tmp13 = S( 1, 1 ) * tmp2 - S( 1, 2 ) * tmp4 + S( 1, 4 ) * tmp6;
    tmp14 = S( 1, 1 ) * tmp3 - S( 1, 2 ) * tmp5 + S( 1, 3 ) * tmp6;
    tmp15 = S( 1, 0 ) * tmp1 - S( 1, 3 ) * tmp7 + S( 1, 4 ) * tmp8;
    tmp16 = S( 1, 0 ) * tmp2 - S( 1, 2 ) * tmp7 + S( 1, 4 ) * tmp9;
    tmp17 = S( 1, 0 ) * tmp3 - S( 1, 2 ) * tmp8 + S( 1, 3 ) * tmp9;
    tmp18 = S( 1, 0 ) * tmp4 - S( 1, 1 ) * tmp7 + S( 1, 4 ) * tmp10;
    tmp19 = S( 1, 0 ) * tmp5 - S( 1, 1 ) * tmp8 + S( 1, 3 ) * tmp10;

    T( 0, 2 ) = S( 0, 1 ) * tmp11 - S( 0, 2 ) * tmp12 + S( 0, 3 ) * tmp13 - S( 0, 4 ) * tmp14;
    T( 1, 2 ) = -S( 0, 0 ) * tmp11 + S( 0, 2 ) * tmp15 - S( 0, 3 ) * tmp16 + S( 0, 4 ) * tmp17;
    T( 2, 2 ) = S( 0, 0 ) * tmp12 - S( 0, 1 ) * tmp15 + S( 0, 3 ) * tmp18 - S( 0, 4 ) * tmp19;

    tmp1 = S( 0, 2 ) * S( 1, 3 ) - S( 0, 3 ) * S( 1, 2 );
    tmp2 = S( 0, 1 ) * S( 1, 3 ) - S( 0, 3 ) * S( 1, 1 );
    tmp3 = S( 0, 1 ) * S( 1, 2 ) - S( 0, 2 ) * S( 1, 1 );
    tmp4 = S( 0, 0 ) * S( 1, 3 ) - S( 0, 3 ) * S( 1, 0 );
    tmp5 = S( 0, 0 ) * S( 1, 2 ) - S( 0, 2 ) * S( 1, 0 );
    tmp6 = S( 0, 0 ) * S( 1, 1 ) - S( 0, 1 ) * S( 1, 0 );
    tmp7 = S( 0, 2 ) * S( 1, 4 ) - S( 0, 4 ) * S( 1, 2 );
    tmp8 = S( 0, 1 ) * S( 1, 4 ) - S( 0, 4 ) * S( 1, 1 );
    tmp9 = S( 0, 0 ) * S( 1, 4 ) - S( 0, 4 ) * S( 1, 0 );
    tmp10 = S( 0, 3 ) * S( 1, 4 ) - S( 0, 4 ) * S( 1, 3 );

    tmp11 = S( 2, 2 ) * tmp10 - S( 2, 3 ) * tmp7 + S( 2, 4 ) * tmp1;
    tmp12 = S( 2, 1 ) * tmp10 - S( 2, 3 ) * tmp8 + S( 2, 4 ) * tmp2;
    tmp13 = S( 2, 1 ) * tmp7 - S( 2, 2 ) * tmp8 + S( 2, 4 ) * tmp3;
    tmp14 = S( 2, 1 ) * tmp1 - S( 2, 2 ) * tmp2 + S( 2, 3 ) * tmp3;
    tmp15 = S( 2, 0 ) * tmp10 - S( 2, 3 ) * tmp9 + S( 2, 4 ) * tmp4;
    tmp16 = S( 2, 0 ) * tmp7 - S( 2, 2 ) * tmp9 + S( 2, 4 ) * tmp5;
    tmp17 = S( 2, 0 ) * tmp1 - S( 2, 2 ) * tmp4 + S( 2, 3 ) * tmp5;

    T( 0, 3 ) = S( 4, 1 ) * tmp11 - S( 4, 2 ) * tmp12 + S( 4, 3 ) * tmp13 - S( 4, 4 ) * tmp14;
    T( 0, 4 ) = -S( 3, 1 ) * tmp11 + S( 3, 2 ) * tmp12 - S( 3, 3 ) * tmp13 + S( 3, 4 ) * tmp14;
    T( 1, 3 ) = -S( 4, 0 ) * tmp11 + S( 4, 2 ) * tmp15 - S( 4, 3 ) * tmp16 + S( 4, 4 ) * tmp17;
    T( 1, 4 ) = S( 3, 0 ) * tmp11 - S( 3, 2 ) * tmp15 + S( 3, 3 ) * tmp16 - S( 3, 4 ) * tmp17;

    tmp18 = S( 2, 0 ) * tmp8 - S( 2, 1 ) * tmp9 + S( 2, 4 ) * tmp6;
    tmp19 = S( 2, 0 ) * tmp2 - S( 2, 1 ) * tmp4 + S( 2, 3 ) * tmp6;
    tmp20 = S( 2, 0 ) * tmp3 - S( 2, 1 ) * tmp5 + S( 2, 2 ) * tmp6;

    T( 2, 3 ) = S( 4, 0 ) * tmp12 - S( 4, 1 ) * tmp15 + S( 4, 3 ) * tmp18 - S( 4, 4 ) * tmp19;
    T( 2, 4 ) = -S( 3, 0 ) * tmp12 + S( 3, 1 ) * tmp15 - S( 3, 3 ) * tmp18 + S( 3, 4 ) * tmp19;
    T( 3, 3 ) = -S( 4, 0 ) * tmp13 + S( 4, 1 ) * tmp16 - S( 4, 2 ) * tmp18 + S( 4, 4 ) * tmp20;
    T( 3, 4 ) = S( 3, 0 ) * tmp13 - S( 3, 1 ) * tmp16 + S( 3, 2 ) * tmp18 - S( 3, 4 ) * tmp20;
    T( 4, 3 ) = S( 4, 0 ) * tmp14 - S( 4, 1 ) * tmp17 + S( 4, 2 ) * tmp19 - S( 4, 3 ) * tmp20;
    T( 4, 4 ) = -S( 3, 0 ) * tmp14 + S( 3, 1 ) * tmp17 - S( 3, 2 ) * tmp19 + S( 3, 3 ) * tmp20;

    tmp11 = S( 3, 1 ) * tmp7 - S( 3, 2 ) * tmp8 + S( 3, 4 ) * tmp3;
    tmp12 = S( 3, 0 ) * tmp7 - S( 3, 2 ) * tmp9 + S( 3, 4 ) * tmp5;
    tmp13 = S( 3, 0 ) * tmp8 - S( 3, 1 ) * tmp9 + S( 3, 4 ) * tmp6;
    tmp14 = S( 3, 0 ) * tmp3 - S( 3, 1 ) * tmp5 + S( 3, 2 ) * tmp6;

    tmp15 = S( 3, 1 ) * tmp1 - S( 3, 2 ) * tmp2 + S( 3, 3 ) * tmp3;
    tmp16 = S( 3, 0 ) * tmp1 - S( 3, 2 ) * tmp4 + S( 3, 3 ) * tmp5;
    tmp17 = S( 3, 0 ) * tmp2 - S( 3, 1 ) * tmp4 + S( 3, 3 ) * tmp6;

    T( 3, 2 ) = S( 4, 0 ) * tmp11 - S( 4, 1 ) * tmp12 + S( 4, 2 ) * tmp13 - S( 4, 4 ) * tmp14;
    T( 4, 2 ) = -S( 4, 0 ) * tmp15 + S( 4, 1 ) * tmp16 - S( 4, 2 ) * tmp17 + S( 4, 3 ) * tmp14;

    return S( 0, 0 ) * T( 0, 0 ) + S( 0, 1 ) * T( 1, 0 ) + S( 0, 2 ) * 
        T( 2, 0 ) + S( 0, 3 ) * T( 3, 0 ) + S( 0, 4 ) * T( 4, 0 );
}

// See also blaze/math/dense/Inversion.h
double invertSmallUnsymmetric6( const auto& S, auto& T )
{
    double tmp1 = S( 4, 4 ) * S( 5, 5 ) - S( 4, 5 ) * S( 5, 4 );
    double tmp2 = S( 4, 3 ) * S( 5, 5 ) - S( 4, 5 ) * S( 5, 3 );
    double tmp3 = S( 4, 3 ) * S( 5, 4 ) - S( 4, 4 ) * S( 5, 3 );
    double tmp4 = S( 4, 2 ) * S( 5, 5 ) - S( 4, 5 ) * S( 5, 2 );
    double tmp5 = S( 4, 2 ) * S( 5, 4 ) - S( 4, 4 ) * S( 5, 2 );
    double tmp6 = S( 4, 2 ) * S( 5, 3 ) - S( 4, 3 ) * S( 5, 2 );
    double tmp7 = S( 4, 1 ) * S( 5, 5 ) - S( 4, 5 ) * S( 5, 1 );
    double tmp8 = S( 4, 1 ) * S( 5, 4 ) - S( 4, 4 ) * S( 5, 1 );
    double tmp9 = S( 4, 1 ) * S( 5, 3 ) - S( 4, 3 ) * S( 5, 1 );
    double tmp10 = S( 4, 1 ) * S( 5, 2 ) - S( 4, 2 ) * S( 5, 1 );
    double tmp11 = S( 4, 0 ) * S( 5, 5 ) - S( 4, 5 ) * S( 5, 0 );
    double tmp12 = S( 4, 0 ) * S( 5, 4 ) - S( 4, 4 ) * S( 5, 0 );
    double tmp13 = S( 4, 0 ) * S( 5, 3 ) - S( 4, 3 ) * S( 5, 0 );
    double tmp14 = S( 4, 0 ) * S( 5, 2 ) - S( 4, 2 ) * S( 5, 0 );
    double tmp15 = S( 4, 0 ) * S( 5, 1 ) - S( 4, 1 ) * S( 5, 0 );

    double tmp16 = S( 3, 3 ) * tmp1 - S( 3, 4 ) * tmp2 + S( 3, 5 ) * tmp3;
    double tmp17 = S( 3, 2 ) * tmp1 - S( 3, 4 ) * tmp4 + S( 3, 5 ) * tmp5;
    double tmp18 = S( 3, 2 ) * tmp2 - S( 3, 3 ) * tmp4 + S( 3, 5 ) * tmp6;
    double tmp19 = S( 3, 2 ) * tmp3 - S( 3, 3 ) * tmp5 + S( 3, 4 ) * tmp6;
    double tmp20 = S( 3, 1 ) * tmp1 - S( 3, 4 ) * tmp7 + S( 3, 5 ) * tmp8;
    double tmp21 = S( 3, 1 ) * tmp2 - S( 3, 3 ) * tmp7 + S( 3, 5 ) * tmp9;
    double tmp22 = S( 3, 1 ) * tmp3 - S( 3, 3 ) * tmp8 + S( 3, 4 ) * tmp9;
    double tmp23 = S( 3, 1 ) * tmp4 - S( 3, 2 ) * tmp7 + S( 3, 5 ) * tmp10;
    double tmp24 = S( 3, 1 ) * tmp5 - S( 3, 2 ) * tmp8 + S( 3, 4 ) * tmp10;
    double tmp25 = S( 3, 1 ) * tmp6 - S( 3, 2 ) * tmp9 + S( 3, 3 ) * tmp10;
    double tmp26 = S( 3, 0 ) * tmp1 - S( 3, 4 ) * tmp11 + S( 3, 5 ) * tmp12;
    double tmp27 = S( 3, 0 ) * tmp2 - S( 3, 3 ) * tmp11 + S( 3, 5 ) * tmp13;
    double tmp28 = S( 3, 0 ) * tmp3 - S( 3, 3 ) * tmp12 + S( 3, 4 ) * tmp13;
    double tmp29 = S( 3, 0 ) * tmp4 - S( 3, 2 ) * tmp11 + S( 3, 5 ) * tmp14;
    double tmp30 = S( 3, 0 ) * tmp5 - S( 3, 2 ) * tmp12 + S( 3, 4 ) * tmp14;
    double tmp31 = S( 3, 0 ) * tmp6 - S( 3, 2 ) * tmp13 + S( 3, 3 ) * tmp14;
    double tmp32 = S( 3, 0 ) * tmp7 - S( 3, 1 ) * tmp11 + S( 3, 5 ) * tmp15;
    double tmp33 = S( 3, 0 ) * tmp8 - S( 3, 1 ) * tmp12 + S( 3, 4 ) * tmp15;
    double tmp34 = S( 3, 0 ) * tmp9 - S( 3, 1 ) * tmp13 + S( 3, 3 ) * tmp15;
    double tmp35 = S( 3, 0 ) * tmp10 - S( 3, 1 ) * tmp14 + S( 3, 2 ) * tmp15;

    double tmp36 = S( 2, 2 ) * tmp16 - S( 2, 3 ) * tmp17 + S( 2, 4 ) * tmp18 - S( 2, 5 ) * tmp19;
    double tmp37 = S( 2, 1 ) * tmp16 - S( 2, 3 ) * tmp20 + S( 2, 4 ) * tmp21 - S( 2, 5 ) * tmp22;
    double tmp38 = S( 2, 1 ) * tmp17 - S( 2, 2 ) * tmp20 + S( 2, 4 ) * tmp23 - S( 2, 5 ) * tmp24;
    double tmp39 = S( 2, 1 ) * tmp18 - S( 2, 2 ) * tmp21 + S( 2, 3 ) * tmp23 - S( 2, 5 ) * tmp25;
    double tmp40 = S( 2, 1 ) * tmp19 - S( 2, 2 ) * tmp22 + S( 2, 3 ) * tmp24 - S( 2, 4 ) * tmp25;
    double tmp41 = S( 2, 0 ) * tmp16 - S( 2, 3 ) * tmp26 + S( 2, 4 ) * tmp27 - S( 2, 5 ) * tmp28;
    double tmp42 = S( 2, 0 ) * tmp17 - S( 2, 2 ) * tmp26 + S( 2, 4 ) * tmp29 - S( 2, 5 ) * tmp30;
    double tmp43 = S( 2, 0 ) * tmp18 - S( 2, 2 ) * tmp27 + S( 2, 3 ) * tmp29 - S( 2, 5 ) * tmp31;
    double tmp44 = S( 2, 0 ) * tmp19 - S( 2, 2 ) * tmp28 + S( 2, 3 ) * tmp30 - S( 2, 4 ) * tmp31;

    T( 0, 0 ) = S( 1, 1 ) * tmp36 - S( 1, 2 ) * tmp37 + S( 1, 3 ) * tmp38 - S( 1, 4 ) * tmp39 + S( 1, 5 ) * tmp40;
    T( 0, 1 ) = -S( 0, 1 ) * tmp36 + S( 0, 2 ) * tmp37 - S( 0, 3 ) * tmp38 + S( 0, 4 ) * tmp39 - S( 0, 5 ) * tmp40;
    T( 1, 0 ) = -S( 1, 0 ) * tmp36 + S( 1, 2 ) * tmp41 - S( 1, 3 ) * tmp42 + S( 1, 4 ) * tmp43 - S( 1, 5 ) * tmp44;
    T( 1, 1 ) = S( 0, 0 ) * tmp36 - S( 0, 2 ) * tmp41 + S( 0, 3 ) * tmp42 - S( 0, 4 ) * tmp43 + S( 0, 5 ) * tmp44;

    double tmp45 = S( 2, 0 ) * tmp20 - S( 2, 1 ) * tmp26 + S( 2, 4 ) * tmp32 - S( 2, 5 ) * tmp33;
    double tmp46 = S( 2, 0 ) * tmp21 - S( 2, 1 ) * tmp27 + S( 2, 3 ) * tmp32 - S( 2, 5 ) * tmp34;
    double tmp47 = S( 2, 0 ) * tmp22 - S( 2, 1 ) * tmp28 + S( 2, 3 ) * tmp33 - S( 2, 4 ) * tmp34;
    double tmp48 = S( 2, 0 ) * tmp23 - S( 2, 1 ) * tmp29 + S( 2, 2 ) * tmp32 - S( 2, 5 ) * tmp35;
    double tmp49 = S( 2, 0 ) * tmp24 - S( 2, 1 ) * tmp30 + S( 2, 2 ) * tmp33 - S( 2, 4 ) * tmp35;

    T( 2, 0 ) = S( 1, 0 ) * tmp37 - S( 1, 1 ) * tmp41 + S( 1, 3 ) * tmp45 - S( 1, 4 ) * tmp46 + S( 1, 5 ) * tmp47;
    T( 2, 1 ) = -S( 0, 0 ) * tmp37 + S( 0, 1 ) * tmp41 - S( 0, 3 ) * tmp45 + S( 0, 4 ) * tmp46 - S( 0, 5 ) * tmp47;
    T( 3, 0 ) = -S( 1, 0 ) * tmp38 + S( 1, 1 ) * tmp42 - S( 1, 2 ) * tmp45 + S( 1, 4 ) * tmp48 - S( 1, 5 ) * tmp49;
    T( 3, 1 ) = S( 0, 0 ) * tmp38 - S( 0, 1 ) * tmp42 + S( 0, 2 ) * tmp45 - S( 0, 4 ) * tmp48 + S( 0, 5 ) * tmp49;

    double tmp50 = S( 2, 0 ) * tmp25 - S( 2, 1 ) * tmp31 + S( 2, 2 ) * tmp34 - S( 2, 3 ) * tmp35;

    T( 4, 0 ) = S( 1, 0 ) * tmp39 - S( 1, 1 ) * tmp43 + S( 1, 2 ) * tmp46 - S( 1, 3 ) * tmp48 + S( 1, 5 ) * tmp50;
    T( 4, 1 ) = -S( 0, 0 ) * tmp39 + S( 0, 1 ) * tmp43 - S( 0, 2 ) * tmp46 + S( 0, 3 ) * tmp48 - S( 0, 5 ) * tmp50;
    T( 5, 0 ) = -S( 1, 0 ) * tmp40 + S( 1, 1 ) * tmp44 - S( 1, 2 ) * tmp47 + S( 1, 3 ) * tmp49 - S( 1, 4 ) * tmp50;
    T( 5, 1 ) = S( 0, 0 ) * tmp40 - S( 0, 1 ) * tmp44 + S( 0, 2 ) * tmp47 - S( 0, 3 ) * tmp49 + S( 0, 4 ) * tmp50;

    tmp36 = S( 1, 2 ) * tmp16 - S( 1, 3 ) * tmp17 + S( 1, 4 ) * tmp18 - S( 1, 5 ) * tmp19;
    tmp37 = S( 1, 1 ) * tmp16 - S( 1, 3 ) * tmp20 + S( 1, 4 ) * tmp21 - S( 1, 5 ) * tmp22;
    tmp38 = S( 1, 1 ) * tmp17 - S( 1, 2 ) * tmp20 + S( 1, 4 ) * tmp23 - S( 1, 5 ) * tmp24;
    tmp39 = S( 1, 1 ) * tmp18 - S( 1, 2 ) * tmp21 + S( 1, 3 ) * tmp23 - S( 1, 5 ) * tmp25;
    tmp40 = S( 1, 1 ) * tmp19 - S( 1, 2 ) * tmp22 + S( 1, 3 ) * tmp24 - S( 1, 4 ) * tmp25;
    tmp41 = S( 1, 0 ) * tmp16 - S( 1, 3 ) * tmp26 + S( 1, 4 ) * tmp27 - S( 1, 5 ) * tmp28;
    tmp42 = S( 1, 0 ) * tmp17 - S( 1, 2 ) * tmp26 + S( 1, 4 ) * tmp29 - S( 1, 5 ) * tmp30;
    tmp43 = S( 1, 0 ) * tmp18 - S( 1, 2 ) * tmp27 + S( 1, 3 ) * tmp29 - S( 1, 5 ) * tmp31;
    tmp44 = S( 1, 0 ) * tmp19 - S( 1, 2 ) * tmp28 + S( 1, 3 ) * tmp30 - S( 1, 4 ) * tmp31;
    tmp45 = S( 1, 0 ) * tmp20 - S( 1, 1 ) * tmp26 + S( 1, 4 ) * tmp32 - S( 1, 5 ) * tmp33;
    tmp46 = S( 1, 0 ) * tmp21 - S( 1, 1 ) * tmp27 + S( 1, 3 ) * tmp32 - S( 1, 5 ) * tmp34;
    tmp47 = S( 1, 0 ) * tmp22 - S( 1, 1 ) * tmp28 + S( 1, 3 ) * tmp33 - S( 1, 4 ) * tmp34;
    tmp48 = S( 1, 0 ) * tmp23 - S( 1, 1 ) * tmp29 + S( 1, 2 ) * tmp32 - S( 1, 5 ) * tmp35;
    tmp49 = S( 1, 0 ) * tmp24 - S( 1, 1 ) * tmp30 + S( 1, 2 ) * tmp33 - S( 1, 4 ) * tmp35;
    tmp50 = S( 1, 0 ) * tmp25 - S( 1, 1 ) * tmp31 + S( 1, 2 ) * tmp34 - S( 1, 3 ) * tmp35;

    T( 0, 2 ) = S( 0, 1 ) * tmp36 - S( 0, 2 ) * tmp37 + S( 0, 3 ) * tmp38 - S( 0, 4 ) * tmp39 + S( 0, 5 ) * tmp40;
    T( 1, 2 ) = -S( 0, 0 ) * tmp36 + S( 0, 2 ) * tmp41 - S( 0, 3 ) * tmp42 + S( 0, 4 ) * tmp43 - S( 0, 5 ) * tmp44;
    T( 2, 2 ) = S( 0, 0 ) * tmp37 - S( 0, 1 ) * tmp41 + S( 0, 3 ) * tmp45 - S( 0, 4 ) * tmp46 + S( 0, 5 ) * tmp47;
    T( 3, 2 ) = -S( 0, 0 ) * tmp38 + S( 0, 1 ) * tmp42 - S( 0, 2 ) * tmp45 + S( 0, 4 ) * tmp48 - S( 0, 5 ) * tmp49;
    T( 4, 2 ) = S( 0, 0 ) * tmp39 - S( 0, 1 ) * tmp43 + S( 0, 2 ) * tmp46 - S( 0, 3 ) * tmp48 + S( 0, 5 ) * tmp50;
    T( 5, 2 ) = -S( 0, 0 ) * tmp40 + S( 0, 1 ) * tmp44 - S( 0, 2 ) * tmp47 + S( 0, 3 ) * tmp49 - S( 0, 4 ) * tmp50;

    tmp1 = S( 0, 3 ) * S( 1, 4 ) - S( 0, 4 ) * S( 1, 3 );
    tmp2 = S( 0, 2 ) * S( 1, 4 ) - S( 0, 4 ) * S( 1, 2 );
    tmp3 = S( 0, 2 ) * S( 1, 3 ) - S( 0, 3 ) * S( 1, 2 );
    tmp4 = S( 0, 1 ) * S( 1, 4 ) - S( 0, 4 ) * S( 1, 1 );
    tmp5 = S( 0, 1 ) * S( 1, 3 ) - S( 0, 3 ) * S( 1, 1 );
    tmp6 = S( 0, 1 ) * S( 1, 2 ) - S( 0, 2 ) * S( 1, 1 );
    tmp7 = S( 0, 0 ) * S( 1, 4 ) - S( 0, 4 ) * S( 1, 0 );
    tmp8 = S( 0, 0 ) * S( 1, 3 ) - S( 0, 3 ) * S( 1, 0 );
    tmp9 = S( 0, 0 ) * S( 1, 2 ) - S( 0, 2 ) * S( 1, 0 );
    tmp10 = S( 0, 0 ) * S( 1, 1 ) - S( 0, 1 ) * S( 1, 0 );
    tmp11 = S( 0, 3 ) * S( 1, 5 ) - S( 0, 5 ) * S( 1, 3 );
    tmp12 = S( 0, 2 ) * S( 1, 5 ) - S( 0, 5 ) * S( 1, 2 );
    tmp13 = S( 0, 1 ) * S( 1, 5 ) - S( 0, 5 ) * S( 1, 1 );
    tmp14 = S( 0, 0 ) * S( 1, 5 ) - S( 0, 5 ) * S( 1, 0 );
    tmp15 = S( 0, 4 ) * S( 1, 5 ) - S( 0, 5 ) * S( 1, 4 );

    tmp16 = S( 2, 3 ) * tmp15 - S( 2, 4 ) * tmp11 + S( 2, 5 ) * tmp1;
    tmp17 = S( 2, 2 ) * tmp15 - S( 2, 4 ) * tmp12 + S( 2, 5 ) * tmp2;
    tmp18 = S( 2, 2 ) * tmp11 - S( 2, 3 ) * tmp12 + S( 2, 5 ) * tmp3;
    tmp19 = S( 2, 2 ) * tmp1 - S( 2, 3 ) * tmp2 + S( 2, 4 ) * tmp3;
    tmp20 = S( 2, 1 ) * tmp15 - S( 2, 4 ) * tmp13 + S( 2, 5 ) * tmp4;
    tmp21 = S( 2, 1 ) * tmp11 - S( 2, 3 ) * tmp13 + S( 2, 5 ) * tmp5;
    tmp22 = S( 2, 1 ) * tmp1 - S( 2, 3 ) * tmp4 + S( 2, 4 ) * tmp5;
    tmp23 = S( 2, 1 ) * tmp12 - S( 2, 2 ) * tmp13 + S( 2, 5 ) * tmp6;
    tmp24 = S( 2, 1 ) * tmp2 - S( 2, 2 ) * tmp4 + S( 2, 4 ) * tmp6;
    tmp25 = S( 2, 1 ) * tmp3 - S( 2, 2 ) * tmp5 + S( 2, 3 ) * tmp6;
    tmp26 = S( 2, 0 ) * tmp15 - S( 2, 4 ) * tmp14 + S( 2, 5 ) * tmp7;
    tmp27 = S( 2, 0 ) * tmp11 - S( 2, 3 ) * tmp14 + S( 2, 5 ) * tmp8;
    tmp28 = S( 2, 0 ) * tmp1 - S( 2, 3 ) * tmp7 + S( 2, 4 ) * tmp8;
    tmp29 = S( 2, 0 ) * tmp12 - S( 2, 2 ) * tmp14 + S( 2, 5 ) * tmp9;
    tmp30 = S( 2, 0 ) * tmp2 - S( 2, 2 ) * tmp7 + S( 2, 4 ) * tmp9;
    tmp31 = S( 2, 0 ) * tmp3 - S( 2, 2 ) * tmp8 + S( 2, 3 ) * tmp9;
    tmp32 = S( 2, 0 ) * tmp13 - S( 2, 1 ) * tmp14 + S( 2, 5 ) * tmp10;
    tmp33 = S( 2, 0 ) * tmp4 - S( 2, 1 ) * tmp7 + S( 2, 4 ) * tmp10;
    tmp34 = S( 2, 0 ) * tmp5 - S( 2, 1 ) * tmp8 + S( 2, 3 ) * tmp10;
    tmp35 = S( 2, 0 ) * tmp6 - S( 2, 1 ) * tmp9 + S( 2, 2 ) * tmp10;

    tmp36 = S( 3, 2 ) * tmp16 - S( 3, 3 ) * tmp17 + S( 3, 4 ) * tmp18 - S( 3, 5 ) * tmp19;
    tmp37 = S( 3, 1 ) * tmp16 - S( 3, 3 ) * tmp20 + S( 3, 4 ) * tmp21 - S( 3, 5 ) * tmp22;
    tmp38 = S( 3, 1 ) * tmp17 - S( 3, 2 ) * tmp20 + S( 3, 4 ) * tmp23 - S( 3, 5 ) * tmp24;
    tmp39 = S( 3, 1 ) * tmp18 - S( 3, 2 ) * tmp21 + S( 3, 3 ) * tmp23 - S( 3, 5 ) * tmp25;
    tmp40 = S( 3, 1 ) * tmp19 - S( 3, 2 ) * tmp22 + S( 3, 3 ) * tmp24 - S( 3, 4 ) * tmp25;
    tmp41 = S( 3, 0 ) * tmp16 - S( 3, 3 ) * tmp26 + S( 3, 4 ) * tmp27 - S( 3, 5 ) * tmp28;
    tmp42 = S( 3, 0 ) * tmp17 - S( 3, 2 ) * tmp26 + S( 3, 4 ) * tmp29 - S( 3, 5 ) * tmp30;
    tmp43 = S( 3, 0 ) * tmp18 - S( 3, 2 ) * tmp27 + S( 3, 3 ) * tmp29 - S( 3, 5 ) * tmp31;
    tmp44 = S( 3, 0 ) * tmp19 - S( 3, 2 ) * tmp28 + S( 3, 3 ) * tmp30 - S( 3, 4 ) * tmp31;

    T( 0, 4 ) = -S( 5, 1 ) * tmp36 + S( 5, 2 ) * tmp37 - S( 5, 3 ) * tmp38 + S( 5, 4 ) * tmp39 - S( 5, 5 ) * tmp40;
    T( 0, 5 ) = S( 4, 1 ) * tmp36 - S( 4, 2 ) * tmp37 + S( 4, 3 ) * tmp38 - S( 4, 4 ) * tmp39 + S( 4, 5 ) * tmp40;
    T( 1, 4 ) = S( 5, 0 ) * tmp36 - S( 5, 2 ) * tmp41 + S( 5, 3 ) * tmp42 - S( 5, 4 ) * tmp43 + S( 5, 5 ) * tmp44;
    T( 1, 5 ) = -S( 4, 0 ) * tmp36 + S( 4, 2 ) * tmp41 - S( 4, 3 ) * tmp42 + S( 4, 4 ) * tmp43 - S( 4, 5 ) * tmp44;

    tmp45 = S( 3, 0 ) * tmp20 - S( 3, 1 ) * tmp26 + S( 3, 4 ) * tmp32 - S( 3, 5 ) * tmp33;
    tmp46 = S( 3, 0 ) * tmp21 - S( 3, 1 ) * tmp27 + S( 3, 3 ) * tmp32 - S( 3, 5 ) * tmp34;
    tmp47 = S( 3, 0 ) * tmp22 - S( 3, 1 ) * tmp28 + S( 3, 3 ) * tmp33 - S( 3, 4 ) * tmp34;
    tmp48 = S( 3, 0 ) * tmp23 - S( 3, 1 ) * tmp29 + S( 3, 2 ) * tmp32 - S( 3, 5 ) * tmp35;
    tmp49 = S( 3, 0 ) * tmp24 - S( 3, 1 ) * tmp30 + S( 3, 2 ) * tmp33 - S( 3, 4 ) * tmp35;

    T( 2, 4 ) = -S( 5, 0 ) * tmp37 + S( 5, 1 ) * tmp41 - S( 5, 3 ) * tmp45 + S( 5, 4 ) * tmp46 - S( 5, 5 ) * tmp47;
    T( 2, 5 ) = S( 4, 0 ) * tmp37 - S( 4, 1 ) * tmp41 + S( 4, 3 ) * tmp45 - S( 4, 4 ) * tmp46 + S( 4, 5 ) * tmp47;
    T( 3, 4 ) = S( 5, 0 ) * tmp38 - S( 5, 1 ) * tmp42 + S( 5, 2 ) * tmp45 - S( 5, 4 ) * tmp48 + S( 5, 5 ) * tmp49;
    T( 3, 5 ) = -S( 4, 0 ) * tmp38 + S( 4, 1 ) * tmp42 - S( 4, 2 ) * tmp45 + S( 4, 4 ) * tmp48 - S( 4, 5 ) * tmp49;

    tmp50 = S( 3, 0 ) * tmp25 - S( 3, 1 ) * tmp31 + S( 3, 2 ) * tmp34 - S( 3, 3 ) * tmp35;

    T( 4, 4 ) = -S( 5, 0 ) * tmp39 + S( 5, 1 ) * tmp43 - S( 5, 2 ) * tmp46 + S( 5, 3 ) * tmp48 - S( 5, 5 ) * tmp50;
    T( 4, 5 ) = S( 4, 0 ) * tmp39 - S( 4, 1 ) * tmp43 + S( 4, 2 ) * tmp46 - S( 4, 3 ) * tmp48 + S( 4, 5 ) * tmp50;
    T( 5, 4 ) = S( 5, 0 ) * tmp40 - S( 5, 1 ) * tmp44 + S( 5, 2 ) * tmp47 - S( 5, 3 ) * tmp49 + S( 5, 4 ) * tmp50;
    T( 5, 5 ) = -S( 4, 0 ) * tmp40 + S( 4, 1 ) * tmp44 - S( 4, 2 ) * tmp47 + S( 4, 3 ) * tmp49 - S( 4, 4 ) * tmp50;

    tmp36 = S( 4, 2 ) * tmp16 - S( 4, 3 ) * tmp17 + S( 4, 4 ) * tmp18 - S( 4, 5 ) * tmp19;
    tmp37 = S( 4, 1 ) * tmp16 - S( 4, 3 ) * tmp20 + S( 4, 4 ) * tmp21 - S( 4, 5 ) * tmp22;
    tmp38 = S( 4, 1 ) * tmp17 - S( 4, 2 ) * tmp20 + S( 4, 4 ) * tmp23 - S( 4, 5 ) * tmp24;
    tmp39 = S( 4, 1 ) * tmp18 - S( 4, 2 ) * tmp21 + S( 4, 3 ) * tmp23 - S( 4, 5 ) * tmp25;
    tmp40 = S( 4, 1 ) * tmp19 - S( 4, 2 ) * tmp22 + S( 4, 3 ) * tmp24 - S( 4, 4 ) * tmp25;
    tmp41 = S( 4, 0 ) * tmp16 - S( 4, 3 ) * tmp26 + S( 4, 4 ) * tmp27 - S( 4, 5 ) * tmp28;
    tmp42 = S( 4, 0 ) * tmp17 - S( 4, 2 ) * tmp26 + S( 4, 4 ) * tmp29 - S( 4, 5 ) * tmp30;
    tmp43 = S( 4, 0 ) * tmp18 - S( 4, 2 ) * tmp27 + S( 4, 3 ) * tmp29 - S( 4, 5 ) * tmp31;
    tmp44 = S( 4, 0 ) * tmp19 - S( 4, 2 ) * tmp28 + S( 4, 3 ) * tmp30 - S( 4, 4 ) * tmp31;
    tmp45 = S( 4, 0 ) * tmp20 - S( 4, 1 ) * tmp26 + S( 4, 4 ) * tmp32 - S( 4, 5 ) * tmp33;
    tmp46 = S( 4, 0 ) * tmp21 - S( 4, 1 ) * tmp27 + S( 4, 3 ) * tmp32 - S( 4, 5 ) * tmp34;
    tmp47 = S( 4, 0 ) * tmp22 - S( 4, 1 ) * tmp28 + S( 4, 3 ) * tmp33 - S( 4, 4 ) * tmp34;
    tmp48 = S( 4, 0 ) * tmp23 - S( 4, 1 ) * tmp29 + S( 4, 2 ) * tmp32 - S( 4, 5 ) * tmp35;
    tmp49 = S( 4, 0 ) * tmp24 - S( 4, 1 ) * tmp30 + S( 4, 2 ) * tmp33 - S( 4, 4 ) * tmp35;
    tmp50 = S( 4, 0 ) * tmp25 - S( 4, 1 ) * tmp31 + S( 4, 2 ) * tmp34 - S( 4, 3 ) * tmp35;

    T( 0, 3 ) = S( 5, 1 ) * tmp36 - S( 5, 2 ) * tmp37 + S( 5, 3 ) * tmp38 - S( 5, 4 ) * tmp39 + S( 5, 5 ) * tmp40;
    T( 1, 3 ) = -S( 5, 0 ) * tmp36 + S( 5, 2 ) * tmp41 - S( 5, 3 ) * tmp42 + S( 5, 4 ) * tmp43 - S( 5, 5 ) * tmp44;
    T( 2, 3 ) = S( 5, 0 ) * tmp37 - S( 5, 1 ) * tmp41 + S( 5, 3 ) * tmp45 - S( 5, 4 ) * tmp46 + S( 5, 5 ) * tmp47;
    T( 3, 3 ) = -S( 5, 0 ) * tmp38 + S( 5, 1 ) * tmp42 - S( 5, 2 ) * tmp45 + S( 5, 4 ) * tmp48 - S( 5, 5 ) * tmp49;
    T( 4, 3 ) = S( 5, 0 ) * tmp39 - S( 5, 1 ) * tmp43 + S( 5, 2 ) * tmp46 - S( 5, 3 ) * tmp48 + S( 5, 5 ) * tmp50;
    T( 5, 3 ) = -S( 5, 0 ) * tmp40 + S( 5, 1 ) * tmp44 - S( 5, 2 ) * tmp47 + S( 5, 3 ) * tmp49 - S( 5, 4 ) * tmp50;

    return S( 0, 0 ) * T( 0, 0 ) + S( 0, 1 ) * T( 1, 0 ) + S( 0, 2 ) * T( 2, 0 ) +
        S( 0, 3 ) * T( 3, 0 ) + S( 0, 4 ) * T( 4, 0 ) + S( 0, 5 ) * T( 5, 0 );
}

void invert( const double* source, double* target, size_t size )
{
    auto S = [=]( size_t i, size_t j ) -> double { return source[i * size + j]; };
    auto T = [=]( size_t i, size_t j ) -> double& { return target[i * size + j]; };

    if( size == 0 )
    {
        return;
    }

    // Direct inverse computation for small matrices
    if( size <= 6 )
    {
        double det = 0.0;

        if( size == 1 ) det = 1.0 / source[0];
        else if( size == 2 ) det = invertSmall2( S, T );
        else if( size == 3 ) det = invertSmallUnsymmetric3( S, T );
        else if( size == 4 ) det = invertSmallUnsymmetric4( S, T );
        else if( size == 5 ) det = invertSmallUnsymmetric5( S, T );
        else if( size == 6 ) det = invertSmallUnsymmetric6( S, T );

        MLHP_CHECK( std::abs( det ) > 1e-12, "Matrix is singular." );

        double invDet = 1.0 / det;

        for( size_t i = 0; i < size * size; ++i )
        {
            target[i] *= invDet;
        }
    }
    else
    {
        MLHP_THROW( "Implement inversion." );
    }
}

} // mlhp::linalg
