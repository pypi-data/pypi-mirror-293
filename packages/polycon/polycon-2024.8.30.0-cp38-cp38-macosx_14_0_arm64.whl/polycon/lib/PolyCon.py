from .type_promote import type_promote, type_name_for_items_of
import numpy
import sys
import os

class PolyCon:
    def __init__( self, a_dirs, a_offs = None, b_dirs = None, b_offs = None ):
        """ a => affine functions, b => boundarys """

        self.all_infinite = 0

        # display parameters
        self.namesv = "xyzabc"
        self.namef = ""

        if 'polycon_bindings_' in repr( type( a_dirs ) ):
            self.ndim = a_dirs.ndim()
            self.pc = a_dirs
            return

        # arg types
        a_dirs = numpy.asarray( a_dirs )
        a_offs = numpy.asarray( a_offs )
        b_dirs = numpy.asarray( b_dirs )
        b_offs = numpy.asarray( b_offs )

        # compile time parameters
        self.dtype = type_promote( [
            type_name_for_items_of( a_dirs ),
            type_name_for_items_of( a_offs ),
            type_name_for_items_of( b_dirs ),
            type_name_for_items_of( b_offs ),
        ], ensure_scalar = True )

        if a_dirs.ndim > 1:
            if b_dirs.ndim > 1:
                if a_dirs.shape[ 1 ] != b_dirs.shape[ 1 ]:
                    raise ValueError( "Incoherent number of dimensions" )
            self.ndim = a_dirs.shape[ 1 ]
        else:
            if b_dirs.ndim > 1:
                self.ndim = b_dirs.shape[ 1 ]
            else:
                self.ndim = 0

        # get the wrapper type
        sys.path.append( os.path.dirname( os.path.abspath( __file__ ) ) )
        try:
            # first try
            self.classv = PolyCon.__cpp_class_for( self.ndim, self.dtype )
        except ModuleNotFoundError:
            # make the source file if not already present
            PolyCon.__make_cpp_file_for( self.ndim, self.dtype )

            # cpp compile/load hook
            import cppimport.import_hook

            # try again
            self.classv = PolyCon.__cpp_class_for( self.ndim, self.dtype )

        # make the new instance
        self.pc = self.classv( a_dirs, a_offs, b_dirs, b_offs )


    @staticmethod
    def from_sym_repr( func, limits, verbose = 0 ):
        """
            for example:
                func = 'max(3*a+2*b-1, 4*a-b+3,7*a-3*b+9)'
                limits = ['a+1 <= 0 ','b >= 1']
        """
        import sympy
        expr_fun = sympy.sympify( func )
        expr_doms = [ sympy.sympify( limit ) for limit in limits ]
        variables = sorted( expr_fun.free_symbols.union( *[ expr_dom.free_symbols for expr_dom in expr_doms ] ), key =lambda x: x.name )
        if verbose:
            print('Variables =' , variables)
        list_y = []
        list_v = []
        for expr in expr_fun.args:
            coeffs = expr.as_coefficients_dict()
            list_y.append([float(coeffs.get(v,0)) for v in variables] )
            list_v.append(-float(coeffs.get(1,0)))
        y_t_k = numpy.array( list_y )
        v_t = numpy.array( list_v )
        if len( limits ) == 0:
            return PolyCon( [ y_t_k[ i ] for i in range( len( y_t_k ) ) ] , [ v_t[ i ]  for i in range( len( v_t ) ) ], [], [] )

        list_ytilde = []
        list_vtilde = []

        for expr in expr_doms:
            lhs, rhs = expr.args
            if expr.func == sympy.core.relational.LessThan or expr.func == sympy.core.relational.StrictLessThan:
                diff = lhs - rhs
            elif expr.func == sympy.core.relational.GreaterThan or expr.func == sympy.core.relational.StrictGreaterThan:
                diff = rhs - lhs
            else:
                print('Not expected format.')
            coeffs = diff.as_coefficients_dict()
            list_ytilde.append( [ float( coeffs.get( v, 0 ) ) for v in variables ] )
            list_vtilde.append( -float( coeffs.get( 1, 0 ) ) )
        ytilde_s_k = numpy.array( list_ytilde )
        vtilde_s = numpy.array( list_vtilde )
        return PolyCon( 
            [ y_t_k[ i ] for i in range( len( y_t_k ) ) ],
            [ v_t[ i ] for i in range( len( v_t ) ) ],
            [ ytilde_s_k[ i ] for i in range( len( ytilde_s_k ) ) ],
            [ vtilde_s[ i ]for i in range( len( vtilde_s ) ) ]
        )        

    @staticmethod
    def __base_file_name_for( ndim, type_name ):
        return "polycon_bindings_{:02}_{}".format( ndim, type_name )

    @staticmethod
    def __class_name_for( ndim, type_name ):
        return "PolyCon_{:02}_{}".format( ndim, type_name )
    
    @staticmethod
    def __cpp_class_for( ndim, type_name ):
        module = __import__( PolyCon.__base_file_name_for( ndim, type_name ) )
        return getattr( module, PolyCon.__class_name_for( ndim, type_name ) )

    @staticmethod
    def __make_cpp_file_for( ndim, type_name, ):
        module = PolyCon.__base_file_name_for( ndim, type_name )
        class_name = PolyCon.__class_name_for( ndim, type_name )
        filename = os.path.join( os.path.dirname( os.path.abspath( __file__ ) ), module + ".cpp" )

        prelim = ''
        if type_name == 'Rational':
            prelim += '#include <PowerDiagram/support/Rational.h>\n'

        src = f"""// cppimport

            #define POLYCON_DIM { ndim }
            #define POLYCON_SCALAR { type_name }
            { prelim }
            #include "polycon_bindings.h"
            
            PYBIND11_MODULE({ module }, m) {{
                fill_polycon_module( m, "{ class_name }" );
            }}
                
            /*
            <%
            import sys, os
            sys.path.append( os.getcwd() + '/polycon/lib' )
            from cppimport_cfg import cppimport_cfg
            setup_pybind11( cfg )
            cppimport_cfg( cfg )
            %>
            */
        """.replace( '            ', '' )

        # return if already written
        if os.path.exists( filename ):
            with open( filename, 'r' ) as f:
                if f.read() == src:
                    return

        # else, write it
        with open( filename, 'w' ) as f:
            f.write( src )

    @staticmethod
    def from_function_samples( function, points, eps = 1e-6, b_dirs = [], b_offs = [] ):
        a_dirs = []
        a_offs = []
        for p in points:
            p = numpy.asarray( p )
            v = function( p )
            g = []
            for d in range( p.size ):
                o = p.copy()
                o[ d ] += eps
                w = function( o )
                g.append( ( w - v ) / eps )
            
            a_offs.append( numpy.dot( g, p ) - v )
            a_dirs.append( g )

        return PolyCon( a_dirs, a_offs, b_dirs, b_offs )

    def value_and_gradient( self, x_or_xs ):
        """ return none if not in a cell """
        # TODO: optimize
        p = numpy.asarray( x_or_xs )
        if p.ndim == 2:
            values = []
            grads = []
            for x in p:
                r = self.value_and_gradient( x )
                values.append( r[ 0 ] )
                grads.append( r[ 1 ] )
            return values, grads
        
        return self.pc.value_and_gradient( p )

    def value_and_gradients( self, x, probe_size = 1e-6 ):
        """ get value at `x` and all possible gradients at `y` such as `norm_2( x - y ) <= probe_size`. return ( none, [] ) if not in a cell """
        p = numpy.asarray( x )
        return self.pc.value_and_gradients( p, probe_size )

    def value( self, x_or_xs ):
        """ return none if not in a cell """
        res = self.value_and_gradient( x_or_xs )
        if res is None:
            return res
        return res[ 0 ]

    def legendre_transform( self ):
        return PolyCon( self.pc.legendre_transform() )

    def star( self ):
        return self.legendre_transform()

    def __add__( self, that ):
        if isinstance( that, PolyCon ):
            return PolyCon( self.pc.add_polycon( that.pc ) )
        return PolyCon( self.pc.add_scalar( that ) )

    def __radd__( self, that ):
        return self.__add__( that )

    def __sub__( self, that ):
        return PolyCon( self.pc.add_scalar( - that ) )

    def __mul__( self, that ):
        assert( that >= 0 )
        return PolyCon( self.pc.mul_scalar( that ) )

    def __rmul__( self, that ):
        return self.__mul__( that )

    def __repr__( self, table = False, num_digits = 5, with_name = True ):
        if table:
            def as_tab( v ):
                import tabulate
                floatfmt = f"+.{ num_digits }f"
                return "  " + tabulate.tabulate( v, tablefmt= "plain", floatfmt = floatfmt ).replace( '\n', '\n  ' )

            f, b = self.as_fb_arrays()
            res  = "Affine functions:\n"
            res += as_tab( f )
            res += "\nBoundaries:\n"
            res += as_tab( b )
            return res

        if self.all_infinite == 1:
            return '+ infinity everywhere'
        elif self.all_infinite == -1:
            return '- infinity everywhere'
        else:
            from sympy import Symbol, Number

            def round_expr( expr, num_digits ):
                return expr.xreplace( { n : round( n, num_digits ) for n in expr.atoms( Number ) } )
                
            
            x_k = [ Symbol( n ) for n in "xyzabcdef"[ 0 : self.ndim ] ]
            y_t_k, v_t, ytilde_s_k, vtilde_s = self.as_fbdo_arrays()
            
            def domain1d( num_digits = 2 ):
                xl = max( [ float( '-inf' ) ] + [ vtilde_s[ s ] / ytilde_s_k[ s ] for s in range( vtilde_s.size ) if ytilde_s_k[ s ] < 0 ] )
                xu = min( [ float( 'inf' ) ] + [ vtilde_s[ s ] / ytilde_s_k[ s ] for s in range( vtilde_s.size ) if ytilde_s_k[ s ] > 0 ] )
                return round( float( xl ), num_digits ), round( float( xu ), num_digits )

            if v_t.size > 1:
                obj = f'max{ str( { round_expr( e, num_digits ) for e in list( y_t_k @ x_k - v_t ) } ) }'
            else:
                obj = str( ( y_t_k @ x_k - v_t )[ 0 ] )
            constrs = [f'{ round_expr( ytilde_s_k[ s, : ] @ x_k,num_digits ) } <= { round( vtilde_s[ s ], num_digits ) }' for s in range( vtilde_s.size ) ]
            vars_str = ''.join( [ str( name ) + ( ',' if i < self.ndim - 1 else '' ) for ( i, name ) in enumerate( x_k ) ] )
            vars_str_with_parenthesis = ( '(' if self.ndim > 1 else '' ) + vars_str + ( ')' if self.ndim > 1 else '' )
            if with_name:
                if self.namef == '':
                    result = 'Function: '
                else:
                    result = self.namef + '(' + vars_str + ')'
            else:
                result = ''
            result += str( obj )
            if self.ndim == 1 and vtilde_s.size > 0:
                result += '\n'+ ( 'Domain: ' + self.namesv[ 0 ] + f' in { domain1d() }')
            elif self.ndim > 1 and vtilde_s.size > 0:
                result += '\n'+ 'Domain: ' + vars_str_with_parenthesis + ' s.t. ' + ( '\n' if vtilde_s.size > 1 else '' )
                for c in constrs:
                    result +=  str( c )+ '\n'
            else: # if there are no constraints
                result += '\n' + str( 'Domain: ' + vars_str_with_parenthesis + ' in R' + ( '^' + str( self.ndim ) if self.ndim > 1 else '' ) +'\n' )
            return result


    def normalized( self, min_measure = 0 ):
        """ return the same PolyCon, with 
            * normalized boundaries,
            * sorted rows for boundaries and affine functions
        """
        return PolyCon( self.pc.normalized( min_measure ) )

    def as_fbdo_arrays( self ):
        """ return four arrays for the affine function and the boundary ones, with directions and offset
            For instance with `f_dir, f_off, b_dir, b_off = pc.as_fb_arrays()`
               `f_dir` => affine function directions (gradients)
               `f_off` => affine function offsets
               `b_dir` => boundary directions
               `b_off` => boundary offsets
        """
        return self.pc.as_fbdo_arrays()

    def as_fb_arrays( self ):
        """ return two arrays, one for the affine function, one for the boundary ones
            For instance with `f, b = pc.as_fb_array()`
               `f[ :, 0:nb_dims ]` => affine function directions (gradients)
               `f[ :, nb_dims ]` => affine function offsets
               `b[ :, 0:nb_dims ]` => boundary directions
               `b[ :, nb_dims ]` => boundary offsets
        """
        return self.pc.as_fb_arrays()

    def write_vtk( self, filename ):
        """ write a vtk file """
        self.pc.write_vtk( filename )
    
    def edge_points( self ):
        """ return an array with the coordinates + type of the vertice
            array[ num_edge, num_vertex, 0 : ndim ] => vertex coords
            array[ num_edge, num_vertex, ndim + 0 ] => vertex height
            array[ num_edge, num_vertex, ndim + 1 ] => nb interior cuts
            array[ num_edge, num_vertex, ndim + 2 ] => nb boundary cuts
            array[ num_edge, num_vertex, ndim + 3 ] => nb infinity cuts
        """
        return self.pc.edge_points()
    
    def plot( self, color = 'b', show = True ):
        """ use matplotlib """
        from matplotlib import pyplot 

        if self.ndim != 1:
            raise NotImplemented

        edges = self.pc.edge_points().tolist()
        for e in edges:
            e.sort()
        edges.sort()

        def app( xs, ys, edge, c ):
            xs.append( ( 1 - c ) * edge[ 0 ][ 0 ] + c * edge[ 1 ][ 0 ] )
            ys.append( ( 1 - c ) * edge[ 0 ][ 1 ] + c * edge[ 1 ][ 1 ] )

        def is_inf( vertex ):
            return vertex[ 4 ] != 0
        
        # regular lines
        xs = []
        ys = []
        app( xs, ys, edges[ 0 ], is_inf( edges[ 0 ][ 0 ] ) / 3 )
        for e in edges:
            app( xs, ys, e, 1 - is_inf( e[ 1 ] ) / 3 )

        pyplot.plot( xs, ys, color = color )

        # dotted lines
        for e in edges:
            xd = []
            yd = []
            if is_inf( e[ 0 ] ):
                app( xd, yd, e, 0.0 )
                app( xd, yd, e, 1/3 )

            if is_inf( e[ 1 ] ):
                app( xd, yd, e, 2/3 )
                app( xd, yd, e, 1.0 )

            pyplot.plot( xd, yd, linestyle = "dotted", color = color )

        if show:
            pyplot.show()
