#include "soci.h"

using namespace std;

int main()
{
    try
    {
        // regular code
    }
    catch (soci::postgresql_soci_error const &e)
    {
        cerr << "PostgreSQL error: " << e.sqlstate()
             << " " << e.what() << endl;
    }
    catch (soci::exception const &e)
    {
        cerr << "Some other error: " << e.what() << endl;
    }
}