// This file is part of the mlhp project. License: See LICENSE

#ifndef MLHP_BINDINGS_HELPER_HPP
#define MLHP_BINDINGS_HELPER_HPP

#include <functional>

#include "mlhp/core/alias.hpp"
#include "mlhp/core/config.hpp"

namespace mlhp::bindings
{

template<typename Return, typename Arg1, typename... Args>
std::vector<Return> callVectorized( const std::function<Return( Arg1, Args... )>& function, 
                                    const std::vector<Arg1>& arg0, 
                                    const std::vector<Args>&... args )
{
    for( auto size : std::array<size_t, sizeof...( args )> { args.size( )... } )
    {
        MLHP_CHECK( size == arg0.size( ), "Inconsistent sizes in vectorized evaluation." );
    }

    auto result = std::vector<Return>( arg0.size( ) );

    #pragma omp parallel for
    for( std::int64_t ii = 0; ii < static_cast<std::int64_t>( arg0.size( ) ); ++ii )
    {
        auto i = static_cast<size_t>( ii );

        result[i] = function( arg0[i], args[i]... );
    }

    return result;
}

template<typename FunctionType, typename Tag = void> class FunctionWrapper;

template<typename ReturnType, typename... Arguments, typename Tag>
class FunctionWrapper<std::function<ReturnType( Arguments... )>, Tag>
{
public:
    using FunctionType = ReturnType( Arguments... );

    static constexpr bool can_vectorize = sizeof...( Arguments ) >= 1 
        and !std::is_same_v<ReturnType, void>;

    FunctionWrapper( ) = default;

    FunctionWrapper( const std::function<FunctionType>& function ) : 
        function_( function ) 
    { }
    
    FunctionWrapper( std::function<FunctionType>&& function ) : 
        function_( std::move( function ) ) 
    { }

    operator std::function<FunctionType>( ) const
    {
        return function_;
    }

    std::function<FunctionType> get( ) const
    {
        return function_;
    }

    ReturnType call( Arguments&&... args )
    { 
        return function_( std::forward<Arguments>( args ) ... ); 
    }

private:
    std::function<FunctionType> function_;
};

template<typename Function>
inline auto wrapFunction( Function&& function )
{
    auto stdfunction = std::function { std::forward<Function>( function ) };

    return FunctionWrapper<decltype(stdfunction)> { std::move( stdfunction ) };
}

template<typename T, typename Tag = void> inline
auto defineFunctionWrapper( pybind11::module& m, const std::string& name )
{
    auto wrapper = pybind11::class_<FunctionWrapper<T, Tag>>( m, name.c_str( ) );

    wrapper.def( pybind11::init<T>( ) );
    wrapper.def( "__call__", &FunctionWrapper<T, Tag>::call );

    return std::make_unique<decltype( wrapper )>( std::move( wrapper ) );
}

template<typename Return, typename T, size_t N, typename Tag = void> inline
auto defineVectorization( pybind11::class_<FunctionWrapper<std::function<Return( std::array<T, N> )>>>& f )
{
    auto recurse = [&]<size_t D, typename... Args>( auto&& self, Args&&... pybindArgs )
    {
        auto str = "array" + std::to_string( D );
        auto pybindArg = pybind11::arg( str.c_str( ) );

        if constexpr( D + 1 < N )
        {
            self.template operator()<D + 1>( self, std::forward<Args>( pybindArgs )..., std::move( pybindArg ) );
        }
        else
        {
            auto call = []( FunctionWrapper<std::function<Return( std::array<T, N> )>>& wrapper,
                            const std::vector<T>& arg0,
                            const std::vector<std::conditional_t<true, T, Args>>&... args )
            {
                for( auto size : std::array<size_t, sizeof...( args )> { args.size( )... } )
                {
                    MLHP_CHECK( size == arg0.size( ), "Inconsistent sizes in vectorized evaluation." );
                }

                auto result = std::vector<Return>( arg0.size( ) );

                #pragma omp parallel for schedule(static)
                for( std::int64_t ii = 0; ii < static_cast<std::int64_t>( arg0.size( ) ); ++ii )
                {
                    auto i = static_cast<size_t>( ii );

                    result[i] = wrapper.call( std::array { arg0[i], args[i]... } );
                }

                return result;
            };

            f.def(  "__call__", call, std::forward<Args>( pybindArgs )..., std::move( pybindArg ) );
        }
    };

    recurse.template operator()<0>( recurse );
}

template<size_t D>
using IntegrationOrderDeterminorWrapper = FunctionWrapper<QuadratureOrderDeterminor<D>>;

template<size_t D>
using ScalarFunctionWrapper = FunctionWrapper<spatial::ScalarFunction<D>>;

template<size_t D>
using SpatialParameterFunctionWrapper = FunctionWrapper<spatial::ParameterFunction<D>>;

struct RealFunctionTag { };

using RealFunctionWrapper = FunctionWrapper<RealFunction, RealFunctionTag>;
using RealFunctionWithDerivativeWrapper = FunctionWrapper<RealFunctionWithDerivative, RealFunctionTag>;

template<size_t D>
using ImplicitFunctionWrapper = FunctionWrapper<ImplicitFunction<D>>;

template<size_t D>
using RefinementFunctionWrapper = FunctionWrapper<RefinementFunction<D>>;

using LinearOperatorWrapper = FunctionWrapper<linalg::LinearOperator>;

template<size_t D>
using ResolutionDeterminorWrapper = FunctionWrapper<ResolutionDeterminor<D>>;

template<size_t D>
using CellMeshCreatorWrapper = FunctionWrapper<CellMeshCreator<D>>;

//! Wrapper for std::vector<double> to prevent conversions to python
class DoubleVector
{
    std::vector<double> data_;
public:
    template<typename... Args>
    DoubleVector( Args&&... args ) noexcept : 
        data_( std::forward<Args>( args )... )
    { }

    std::vector<double>& get( )
    {
        return data_;
    }

    const std::vector<double>& get( ) const
    {
        return data_;
    }

    size_t size( ) const
    {
        return data_.size( );
    }
};

class ScalarDouble
{
    double value_;

public:
    explicit ScalarDouble( ) : ScalarDouble { 0.0 } { }
    explicit ScalarDouble( double value ) : value_ { value } { }

    double& get( ) { return value_; }
    const double& get( ) const { return value_; }
};

template<size_t D>
auto add( const std::string& str )
{
    return str + std::to_string( D ) + "D";
}

// namespace detail
// {
// 
// template<template<size_t> typename T, typename>
// struct DimensionVariantHelper { };
// 
// template<template<size_t> typename T, size_t... D>
// struct DimensionVariantHelper<T, std::index_sequence<D...>> 
// { 
//     using type = std::variant<T<D + 1>...>; 
// };
// 
// } // namespace detail
// 
// template<template<size_t> typename T, size_t D = config::maxdegree>
// using DimensionVariant = typename detail::DimensionVariantHelper<T, decltype( std::make_index_sequence<4>( ) )>::type;

template<template<size_t> typename T>
using DimensionVariant = std::variant<
    #define MLHP_INSTANTIATE_DIM( D ) \
        T<D>,
    MLHP_DIMENSIONS_XMACRO_LIST
    #undef MLHP_INSTANTIATE_DIM
    int>;

template<template<size_t> typename T>
using DimensionVariantPlus1 = std::variant<
    #define MLHP_INSTANTIATE_DIM( D ) \
        T<D>,
    MLHP_DIMENSIONS_XMACRO_LIST MLHP_INSTANTIATE_DIM( ( config::maxdim + 1 ) )
    #undef MLHP_INSTANTIATE_DIM
    int>;

// template<size_t maxdim, typename T1, typename T2>
// struct FillTable
// {
//     T1& create;
//     T2& table;
// 
//     template<size_t D>
//     void recurse( )
//     {
//         table[D] = create.template operator()<D>( );
// 
//         if constexpr ( D < maxdim )
//         {
//             recurse<D + 1>( );
//         }
//     }
// };
// 
// template<size_t ndim = config::maxdim> inline
// auto createDimensionDispatch( auto&& create )
// {
//     using Create = decltype ( std::function { create.template operator()<1>( ) } );
// 
//     auto table = std::array<Create, ndim + 1> { };
//     auto assign = FillTable<ndim, decltype( create ), decltype( table )> { create, table };
// 
//     assign.template recurse<1>( );
// 
//     return [table = std::move( table )]( size_t D ) -> auto&
//     {
//         MLHP_CHECK( D >= 1 && D < table.size( ), "Invalid number "
//             "of dimensions: " + std::to_string( D ) + "." );
// 
//         return table[D];
//     };
// }

template<size_t ndim = config::maxdim>
auto dispatchDimension( auto&& callback, size_t dim, auto&&... args )
{
    #define MLHP_INSTANTIATE_DIM( D )                        \
        if constexpr ( ndim >= D ) if( dim == D )            \
        {                                                    \
            return callback.template operator()<D> (         \
                std::forward<decltype( args )>( args )... ); \
        }
        MLHP_DIMENSIONS_XMACRO_LIST MLHP_INSTANTIATE_DIM( ( config::maxdim + 1 ) )
    #undef MLHP_INSTANTIATE_DIM

    MLHP_THROW( "Invalid dimension " + std::to_string( dim ) + 
        " with maximum number of dimensions " + std::to_string( ndim ) + "." );
}

} // mlhp::bindings

#endif // MLHP_BINDINGS_HELPER_HPP

