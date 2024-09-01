# AsyncURLCrawler
`AsyncURLCrawler` navigates through web pages concurrently by following hyperlinks to collect URLs.
`AsyncURLCrawler` uses `BFS algorithm`. To make use of it check `robots.txt` of the domains first.

**👉 For complete documentation read [here](https://asyncurlcrawlerdocs.pages.dev/)**

**👉 Source code on Github [here](https://github.com/PouyaEsmaeili/AsyncURLCrawler)**

---

### Install Pacakge

```commandline 
pip install AsyncURLCrawler
```

```commandline 
pip install AsyncURLCrawler==<version>
```

👉 The official [page](https://pypi.org/project/AsyncURLCrawler) of the project in PyPi.

---

### Usage Example in Code

Here is a simple python script to show how to use the package:

```python
import asyncio
import os
from AsyncURLCrawler.parser import Parser
from AsyncURLCrawler.crawler import Crawler
import yaml


async def main():
    parser = Parser(
        delay_start=0.1, 
        max_retries=5, 
        request_timeout=1,
        user_agent="Mozilla",
    )
    crawler = Crawler( 
        seed_urls=["https://pouyae.ir"],
        parser=parser,
        exact=True,
        deep=False,
        delay=0.1,
    )
    result = await crawler.crawl()
    with open(
            os.path.join(output_path, 'result.yaml'), 'w') as file:
        for key in result:
            result[key] = list(result[key])
        yaml.dump(result, file)


if __name__ == "__main__":
    asyncio.run(main())
```

This is the output for the above code:
```yaml
https://pouyae.ir:
- https://github.com/PouyaEsmaeili/AsyncURLCrawler
- https://pouyae.ir/images/pouya3.jpg
- https://github.com/PouyaEsmaeili/CryptographicClientSideUserState
- https://github.com/PouyaEsmaeili/RateLimiter
- https://pouyae.ir/
- https://github.com/luizdepra/hugo-coder/
- https://duman.pouyae.ir/
- https://pouyae.ir/projects/
- https://pouyae.ir/images/pouya4.jpg
- https://pouyae.ir/images/pouya5.jpg
- https://pouyae.ir/gallery/
- https://github.com/PouyaEsmaeili
- https://pouyae.ir/blog/
- https://www.linkedin.com/in/pouya-esmaeili-9124b839/
- https://pouyae.ir/about/
- https://stackoverflow.com/users/13118327/pouya-esmaeili?tab=profile
- https://pouyae.ir/contact-me/
- https://github.com/PouyaEsmaeili/SnowflakeID
- https://pouyae.ir/images/pouya2.jpg
- https://github.com/PouyaEsmaeili/gFuzz
- https://linktr.ee/pouyae
- https://gohugo.io/
- https://pouyae.ir/images/pouya1.jpg
```

👉 There is also a blog post about using `AsyncURLCrawler` to find malicious URLs in a web page. [Read here](https://towardsdev.com/viruscan-a-website-for-malicious-url-with-asyncurlcrawler-and-virus-total-2adaef0201c3?source=friends_link&sk=b537f4ab5387b8172d70b73c933412d1).

---
### Commandline Tool

The script can be customized using the `src/cmd/cmd.py` file, which accepts various arguments to configure the crawler's behavior:

| argument  | description         | 
|-----------|---------------------| 
| `--url`   | Specifies a list of URLs to crawl. At least one URL must be provided. | 
| `--exact` | Optional flag; if set, the crawler will restrict crawling to the specified subdomain/domain only. Default is False.                    | 
| `--deep`  | Optional flag; if enabled, the crawler will explore all visited URLs. Not recommended due to potential resource intensity. If --deep is True, the --exact flag is ignored. | 
| `--delay` | Sets the delay between consecutive HTTP requests, in seconds. |
| `--output`| Specifies the path for the output file, which will be saved in YAML format. |

---

### Run Commandline Tool in Docker Container 🐳

There is a Dockerfile in `src/cmd` to run the above-mentioned cmd tool in a docker container.

```commandline 
docker build -t crawler .
```

```commandline
docker run -v my_dir:/src/output --name crawler crawler
```

After execution of the container, 
the resulting output file will be accessible in the directory named `my_dir` as defined in the above.
To configure the tool based on your needs check the `CMD` in `Dockerfile`.

---

### Build and Publish to Python Package Index(PyPi)

Requirements:

```commandline
python3 -m pip install --upgrade build
```

```commandline
python3 -m pip install --upgrade twine
```
👉 For more details check [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

Build and upload:

```commandline 
python3 -m build
```

```commandline
python3 -m twine upload --repository pypi dist/*
```

---

### Build Documentation with Sphinx

Install packages listed in `docs/doc-requirements.txt`.

```commandline
cd docs
```

```commandline
pip install -r doc-requirements.txt
```

```commandline
make clean
```

```commandline
make html
```

HTML files will be generated in `docs/build`. Push them the repository and deploy on _pages.dev_.

---

### Workflow

- Branch off, implement features and merge them to `main`. Remove feature branches.
- Update version in `pyproject.toml` and push to `main`.
- Add release tag in [Github](https://github.com/PouyaEsmaeili/AsyncURLCrawler/releases).
- Build and push the package to [PyPi](https://pypi.org/project/AsyncURLCrawler/). 
- Build documentation and push HTML files to [AsyncURLCrawlerDocs repo](https://github.com/PouyaEsmaeili/AsyncURLCrawlerDocs)
- Documentation will be deployed on [pages.dev](https://asyncurlcrawlerdocs.pages.dev/) automatically.

---

### Contact

**[Find me @ My Homepage](https://pouyae.ir)**

---

### Disclaimer

**⚠️ Use at your own risk. The author and contributors are not responsible for any misuse or consequences resulting from the use of this project.**

--- 
