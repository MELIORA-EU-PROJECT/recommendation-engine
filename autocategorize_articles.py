import glob

import requests
import html2text

article = """
<article class="sf-detail-body-container sf-detail-body-wrapper activity--detail dynamic-content dynamic-content__article">
    <script type="text/javascript" src="/ResourcePackages/WHO/assets/dist/scripts/multimedia-modal.min.js?v=14.0.7729.22240"></script>
    <script type="text/javascript" src="/ResourcePackages/WHO/assets/dist/scripts/magnific-popup.min.js?v=14.0.7729.22240"></script>
    <script async="" defer="" src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&amp;version=v3.2"></script>
    <header class="dynamic-content__header dynamic-content__container">
        
        <div class="sf-header-image dynamic-content__image dynamic-content__image" data-url="">
            <div class="inner">
                    <a class="magnific-popup" href="https://cdn.who.int/media/images/default-source/tobacco/mpower-banners/offeringe6da62ee-f3a0-4ad2-9e18-066202d4bb35.tmb-1366v.png?sfvrsn=76ff6153_2 1366w" title="WHO Offering help to quit tobacco use">
                        <img sizes="(max-width: 479px) 280px,
                                    (max-width: 549px) 440px,
                                    (max-width: 768px) 660px,
                                    (max-width: 1366px) 1024px,
                                    1920px" srcset="https://cdn.who.int/media/images/default-source/tobacco/mpower-banners/offeringe6da62ee-f3a0-4ad2-9e18-066202d4bb35.tmb-479v.png?sfvrsn=76ff6153_2 479w,
                                     https://cdn.who.int/media/images/default-source/tobacco/mpower-banners/offeringe6da62ee-f3a0-4ad2-9e18-066202d4bb35.tmb-549v.png?sfvrsn=76ff6153_2 549w,
                                     https://cdn.who.int/media/images/default-source/tobacco/mpower-banners/offeringe6da62ee-f3a0-4ad2-9e18-066202d4bb35.tmb-768v.png?sfvrsn=76ff6153_2 768w,
                                     https://cdn.who.int/media/images/default-source/tobacco/mpower-banners/offeringe6da62ee-f3a0-4ad2-9e18-066202d4bb35.tmb-1024v.png?sfvrsn=76ff6153_2 1024w,
                                     https://cdn.who.int/media/images/default-source/tobacco/mpower-banners/offeringe6da62ee-f3a0-4ad2-9e18-066202d4bb35.tmb-1366v.png?sfvrsn=76ff6153_2 1366w,
                                     https://cdn.who.int/media/images/default-source/tobacco/mpower-banners/offeringe6da62ee-f3a0-4ad2-9e18-066202d4bb35.tmb-1920v.png?sfvrsn=76ff6153_2 1920w" class="single-image" alt="Quitting tobacco">
                    </a>
            </div>




    <div class="sf-image-credit desktop-medium" style="display: block;">
        
        <div class="sf-image-credit__content">
            <div class="sf-image-credit__inner">
WHO
                    <br>Offering help to quit tobacco use            </div>
        </div>
        
        <div class="sf-image-credit__label">
            <span class="sf-image-credit__copyright">©</span>
            <span class="sf-image-credit__text">Credits </span>

            <i class="icon plus-icon"></i>
        </div>
    </div>
    <script>
        var imageCreditClass = document.getElementsByClassName("sf-image-credit");

        var preventFunction = function () {
            event.preventDefault()
        };

        for (var i = 0; i < imageCreditClass.length; i++) {
            imageCreditClass[i].addEventListener('click', preventFunction);;
        }
    </script>
        </div>
        
        <div class="dynamic-content__title">
            <h1 class="dynamic-content__title-text">Quitting tobacco</h1>
        </div>
    </header>
    <section class="sf-body-detail container">
        <div class="row">
            <div class="sf_colsIn col-md-12">
                <div class="row sf-content-detail">
                    
                    <div class="sf_colsIn col-md-7">
                            <div class="large-body-font-size">
                                <p>Among smokers who are aware of the dangers of tobacco, most want to quit. Counselling and medication can more than double a tobacco user's chance of successfully quitting. Currently however, only 23 countries provide comprehensive cessation services with full or partial cost-coverage to assist tobacco users to quit. This represents just 32% of the world's population.</p><p>Health professionals have the greatest potential of any group in society to promote the reduction of tobacco use. Studies show that few people understand the specific health risks of tobacco which include lung cancer, heart disease and stroke.&nbsp; Brief advice from health professionals can increase quitting success rates by up to 30%, while intensive advice increases the chance of quitting by 84%.&nbsp;</p><p>Under WHO’s <a href="https://apps.who.int/iris/bitstream/handle/10665/42811/9241591013.pdf" data-sf-ec-immutable="">Framework Convention on Tobacco Control (FCTC)</a>, countries are mandated to treat tobacco use and dependence.&nbsp;WHO provides capacity building and training packages to help governments establish or strengthen their national tobacco cessation systems including integrating brief tobacco interventions into their primary care systems, developing national toll-free quit lines and mCessation projects. Offering help to quit is also one of the five key interventions in the MPOWER package of technical measures and resources which WHO introduced in 2007.</p>
                            </div>
                    </div>
                    
                    <div class="sf_colsIn col-sm-12 col-md-4 col-md-push-1 empty"></div>
                </div>
            </div>
        </div>
    </section>
    <section class="sf-related-detail container">
        <div class="row">
            <div class="sf_colsIn col-md-12 empty"></div>
        </div>
    </section>
</article>
"""


def extract_beh_stages(article: str) -> [[str], [int]]:
    article_ = html2text.html2text(article)
    # print(article_)

    LLAMA_URL = "http://localhost:11434/api/generate"
    res = requests.post(LLAMA_URL, json={
        "model": "autocategorize_simple",
        "prompt": article_,
        "stream": False,
    })

    llama_res: str = res.json()["response"]
    print(llama_res)
    beh_token = "\"behaviours\": "
    beh_start = llama_res.find(beh_token)
    beh_end = llama_res.find("\n", beh_start)

    stages_token = "\"ttm_stages\": "
    stages_start = llama_res.find(stages_token)
    stages_end = llama_res.find("\n", stages_start)
    behaviours = llama_res[beh_start + len(beh_token):beh_end]
    stages = llama_res[stages_start + len(stages_token):stages_end]
    print(f"Behaviours: {behaviours}")
    print(f"Stages: {stages}")
    return behaviours, stages


def main():
    articles = glob.glob("articles/*.html")
    print(articles)

    results = []
    for article in articles:
        with open(article, "r") as f:
            title = article.split("/")[-1].split(".")[0]
            article_ = f.read()
            behaviours, stages = extract_beh_stages(article_)
            results.append((title, behaviours, stages))

    for title, behaviours, stages in results:
        print(f"Title: {title}")
        print(f"Behaviours: {behaviours}")
        print(f"Stages: {stages}")
        print("-" * 50)

    print(f"Number of articles: {len(articles)}")
    print(f"Number of results: {len(results)}")


def test():
    LLAMA_URL = "http://localhost:11434/api/generate"
    res = requests.post(LLAMA_URL, json={
        "model": "autocategorize",
        # "prompt": "What is your name",
        "prompt": "How many states are there in the USA",
        "stream": False,
    })

    print(res.json()["response"])


if __name__ == "__main__":
    main()
    # test()