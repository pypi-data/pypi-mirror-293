// This file is part of the mlhp project. License: See LICENSE

#include "tests/core/core_test.hpp"

#include "mlhp/core/spatial.hpp"
#include "mlhp/core/integrands.hpp"
#include "mlhp/core/basisevaluation.hpp"
#include "mlhp/core/dense.hpp"
#include "mlhp/core/mapping.hpp"

namespace mlhp
{

TEST_CASE( "linearIntegrands_test" )
{ 
    BasisFunctionEvaluation<3> shapes;

    size_t ndof = 5;

    shapes.initialize( 0, 1, 1 );
    shapes.addDofs( 0, ndof );
    shapes.allocate( );

    auto npadded = memory::paddedLength<double>( ndof );

    std::iota( shapes.get( 0, 0 ), shapes.get( 0, 1 ), 0.7 );
    std::iota( shapes.get( 0, 1 ) + 0 * npadded, shapes.get( 0, 1 ) + 1 * npadded, 2.3 );
    std::iota( shapes.get( 0, 1 ) + 1 * npadded, shapes.get( 0, 1 ) + 2 * npadded, 10.3 );
    std::iota( shapes.get( 0, 1 ) + 2 * npadded, shapes.get( 0, 1 ) + 3 * npadded, 18.3 );

    double tolerance = 1e-12;

    auto function1 = []( std::array<double, 3> xyz ) noexcept
    { 
        return spatial::norm( xyz ) + 1.0;
    };

    auto function2 = []( std::array<double, 3> source ) noexcept
    {
        return std::sin( source[0] ) + 
               std::sin( source[1] ) + 
               std::sin( source[2] ) + 2.0;
    };

    std::array<double, 3> rst { 0.2, 0.6, -0.4 };
    std::array<double, 3> xyz { 2.3, -1.8, 3.1 };

    shapes.setRst( rst );
    shapes.setXyz( xyz );

    double weight = 3.12;

    auto paddedNdof = memory::paddedLength<double>( ndof );

    auto storageSize = linalg::denseMatrixStorageSize<linalg::SymmetricDenseMatrix>( ndof );

    auto targets = std::vector
    {
        memory::AlignedVector<double>( storageSize, 0.23 ),
        memory::AlignedVector<double>( paddedNdof, 0.74 )
    };

    auto mapping = MeshMapping<3> { };

    std::vector<double> expectedLhs, expectedRhs;

    SECTION( "Poisson" )
    {
        auto integrand = makePoissonIntegrand<3>( function1, function2 );

        CHECK( integrand.maxdiff == DiffOrders::FirstDerivatives );

        auto cache = integrand.createCache( );

        integrand.prepare( cache, mapping, { } );

        REQUIRE_NOTHROW( integrand.evaluate( cache, shapes, targets, weight ) );

        expectedLhs =
        {
            7.322814080529e+3, 7.829834153777e+3, 8.336854227025e+3, 8.843874300272e+3, 9.350894373520e+3,
            7.829834153777e+3, 8.386079476854e+3, 8.942324799932e+3, 9.498570123010e+3, 1.005481544608e+4,
            8.336854227025e+3, 8.942324799932e+3, 9.547795372840e+3, 1.015326594574e+4, 1.075873651865e+4,
            8.843874300272e+3, 9.498570123010e+3, 1.015326594574e+4, 1.080796176848e+4, 1.146265759122e+4,
            9.350894373520e+3, 1.005481544608e+4, 1.075873651865e+4, 1.146265759122e+4, 1.216657866379e+4
        };

        expectedRhs =
        {
            4.700549124310e+0, 1.035847644475e+1, 1.601640376519e+1, 2.167433108564e+1, 2.733225840608e+1
        };
    }

    SECTION( "L2" )
    {
        auto integrand = makeL2DomainIntegrand<3>( function1, function2 );

        CHECK( integrand.maxdiff == DiffOrders::Shapes );
    
        auto cache = integrand.createCache( );

        integrand.prepare( cache, mapping, { } );

        REQUIRE_NOTHROW( integrand.evaluate( cache, shapes, targets, weight ) );

        expectedLhs =
        {
            8.270124138882e+0, 1.975601576585e+1, 3.124190739283e+1, 4.272779901980e+1, 5.421369064678e+1,
            1.975601576585e+1, 4.765032400279e+1, 7.554463223974e+1, 1.034389404766e+2, 1.313332487136e+2,
            3.124190739283e+1, 7.554463223974e+1, 1.198473570866e+2, 1.641500819335e+2, 2.084528067804e+2,
            4.272779901980e+1, 1.034389404766e+2, 1.641500819335e+2, 2.248612233904e+2, 2.855723648472e+2,
            5.421369064678e+1, 1.313332487136e+2, 2.084528067804e+2, 2.855723648472e+2, 3.626919229141e+2
        };

        expectedRhs =
        {
            4.700549124310e+0, 1.035847644475e+1, 1.601640376519e+1, 2.167433108564e+1, 2.733225840608e+1
        };

    }

    size_t offset = 0;

    for( size_t i = 0; i < ndof; ++i )
    {
        for( size_t j = 0; j <= i; ++j )
        {
            CHECK( targets[0][offset + j] == Approx( expectedLhs[i * ndof + j] ).epsilon( tolerance ) );
        }

        CHECK( targets[1][i] == Approx( expectedRhs[i] ).epsilon( tolerance ) );

        offset += memory::paddedLength<double>( i + 1 );
    }
}

TEST_CASE( "evaluateSolution_test" )
{
    std::vector<double> N =
    {
        4.0, 3.0, 7.0, -0.5, 2.0
    };

    std::vector<double> dN =
    {
        3.7,  9.6, -8.0, -6.2,  0.2,
        8.1, -2.0,  1.7,  2.3,  7.0,
       -5.1,  6.7,  5.8, -0.8, -6.5
    };

    std::vector<double> dofs
    {
        7.3, -5.3,  4.0,  4.3, -1.9,  
        4.9,  4.2, -3.8,  2.1, -9.3, 
       -5.3, -0.9,  7.8,  8.2, -3.0
    };

    LocationMap locationMap
    {
        3, 4, 9, 11, 14
    };
  
    auto ndof = N.size( );
    auto ndofpadded = memory::paddedLength<double>( ndof );

    BasisFunctionEvaluation<3> shapes;

    shapes.initialize( 0, 1, 1 );
    shapes.addDofs( 0, ndof );
    shapes.allocate( );

    for( size_t i = 0; i < ndof; ++i )
    {
        shapes.get( 0, 0 )[i] = N[i];

        shapes.get( 0, 1 )[0 * ndofpadded + i] = dN[0 * ndof + i];
        shapes.get( 0, 1 )[1 * ndofpadded + i] = dN[1 * ndof + i];
        shapes.get( 0, 1 )[2 * ndofpadded + i] = dN[2 * ndof + i];
    }

    auto u = evaluateSolution( shapes, locationMap, dofs );
    auto du = evaluateGradient( shapes, locationMap, dofs );

    CHECK( u == Approx( -59.15 ).epsilon( 1e-13 ) );

    CHECK( du[0] == Approx(  77.05 ).epsilon( 1e-13 ) );
    CHECK( du[1] == Approx( -0.25  ).epsilon( 1e-13 ) );
    CHECK( du[2] == Approx( -68.38 ).epsilon( 1e-13 ) );
}

} // namespace mlhp
