#include <vector>
#include <string>
#include <iostream>
#include "export_cfg.hpp"
#include "Feed.hpp"

int main(int argc, char* argv[]){
    std::vector<std::string> args(argv, argv + argc);

    try
    {
        // init once per process, needed by xerces and curl
        FeedReader::Feed::Initialize();
        FeedReader::Feed feedReader(args[1]);

        // check feed - retrieves and parses results.
        // we can repeat this step as often as we wish to
        // update feed results, but it is recommended to
        // take the value of the TTL feed element into account.
        // when available, the TTL element is a way for the server
        // to tall us the minimal recommended refresh interval.
        feedReader.CheckFeed();

        // get results
        std::cout << "----------Feed---------" << std::endl
             << "URL: '" << feedReader.GetUrl() << "'" << std::endl;

        // print elements (feed level information)
        for (auto fitr = feedReader.begin_feed_elements();
             fitr != feedReader.end_feed_elements(); fitr++)
        {
            std::cout << fitr->first << ":	'" <<  fitr->second << "'" << std::endl;
        }

        // print items(post level information)
        for(auto itr = feedReader.begin_entries();
            itr != feedReader.end_entries(); itr++)
        {
            std::cout << "Item ID: '"	<< itr->UniqueId	<< "'" << std::endl
                      << "IsLive: '"	<< itr->IsLive		<< "'" << std::endl;
            itr->Print(std::cout);
        }
    }
    catch (std::exception& e)
    {
        std::cout << "Exception: " << e.what() << "\n";
    }
    catch (...)
    {
        std::cout << "Unknown exception." << "\n";
    }

    return 0;
}
