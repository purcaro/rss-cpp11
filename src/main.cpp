#include <vector>
#include <string>
#include <iostream>
#include "export_cfg.hpp"
#include "Feed.hpp"
#include <pugixml.hpp>

class ParseRSS{
    FeedReader::FeedConfig config_;

public:
    ParseRSS(){
        // init once per process, needed by xerces and curl
        FeedReader::Feed::Initialize();

        config_ = FeedReader::FeedConfig("/home/mjp/feed-reader-lib/xsl");
    }

    void read(std::string url){
        FeedReader::Feed feedReader(url, config_);

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

        return;

        // print elements (feed level information)
        for(const auto& e : feedReader.FeedLevelElements()){
            std::cout << e.first << ": '"
                      << e.second << "'" << std::endl;
        }

        // print items(post level information)
        for(auto itr = feedReader.begin_entries();
            itr != feedReader.end_entries(); itr++){
            std::cout << "Item ID: '" << itr->UniqueId << "'"
                      << std::endl
                      << "IsLive: '" << itr->IsLive << "'" << std::endl;
            itr->Print(std::cout);
        }
    }
};

std::vector<std::string> parseOpml(){
    pugi::xml_document doc;
    doc.load_file("/home/mjp/Dropbox/rss/subscriptions.opml");
    auto r = doc.select_nodes("//outline");

    std::vector<std::string> urls;
    for(const auto& xmlNode : r){
        const auto& n = xmlNode.node();
        if(std::string("rss") == n.attribute("type").value()){
            auto url = n.attribute("xmlUrl").value();
            if(std::string("") == url){
                std::cerr << "could not find url: " << std::endl;
                n.print(std::cout);
            }
            urls.push_back(url);
        }
    }
    return urls;
}

int main(int argc, char* argv[]){
    std::vector<std::string> args(argv, argv + argc);

    auto urls = parseOpml();

    ParseRSS parser;

    for(const auto& url : urls){
        try {
            std::cout << url << std::endl;
            parser.read(url);
        } catch(...){
            std::cerr << "failed reading \n\t" << url << std::endl;
        }
/*
  catch (std::exception& e)
  {
  std::cout << "Exception: " << e.what() << "\n";
  }
  catch (...)
  {
  std::cout << "Unknown exception." << "\n";
  }
*/
    }

    return 0;
}
