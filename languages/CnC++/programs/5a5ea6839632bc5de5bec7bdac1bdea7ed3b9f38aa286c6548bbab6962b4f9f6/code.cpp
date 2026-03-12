#include <cnc/cnc.h>
#include <iostream>
#include <cstdlib>

struct FibContext;

struct FibStep {
    int execute( const int & t, FibContext & c ) const;
};

struct FibContext : public CnC::context< FibContext >
{
    CnC::step_collection< FibStep > m_steps;
    CnC::item_collection< int, long long > m_fibs;
    CnC::tag_collection< int > m_tags;

    FibContext()
        : CnC::context< FibContext >(),
          m_steps( *this ),
          m_fibs( *this ),
          m_tags( *this )
    {
        m_tags.prescribes( m_steps, *this );
    }
};

int FibStep::execute( const int & t, FibContext & c ) const
{
    if( t <= 1 ) {
        c.m_fibs.put( t, t );
    } else {
        long long f1, f2;
        c.m_fibs.get( t - 1, f1 );
        c.m_fibs.get( t - 2, f2 );
        c.m_fibs.put( t, f1 + f2 );
    }
    return CnC::CNC_Success;
}

int main( int argc, char * argv[] )
{
    int n = ( argc > 1 ) ? atoi( argv[1] ) : 10;
    FibContext c;
    for( int i = 0; i <= n; i++ ) {
        c.m_tags.put( i );
    }
    c.wait();
    long long result;
    c.m_fibs.get( n, result );
    std::cout << "fib(" << n << ") = " << result << std::endl;
    return 0;
}
