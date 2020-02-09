# blog_transformer
Tool for markdown blog migrate

# Description
This tool do the things below:

1. Input a markdown file, download all pictures from "\!\[\]\(https://xxx.xxx\)", saved as {%d}.xxx
2. Modify the "\!\[\]\(https://xxx.xxx\)" to the request form(for example, \{\{\<figure src = "{0}" title = "" lightbox = "true">\}\} which is required by [Hugo](https://sourcethemes.com/academic/docs/writing-markdown-latex/#images))

For example:

Input markdown:


![](res/2020-02-08-16-46-15.png)


Output markdown:


![](res/2020-02-08-16-46-47.png)


In the same time, 0.png is downloaded into the path where Input markdown file exist.

# Usage
## Use blog_transformer

```bash
python3 blog_transformer.py -f YorMarkdown.md
```
or import to python

```python
from blog_transformer import BlogTransformer
bt = BlogTransformer()
md = bt.run(YOUR_FILE_NAME, save_path=YOUR_DIR, save=True)
```
## Use pipeline
Pipeline tool based on blog_transformer, it is a tool for blog building with specified header templete (here "templete.md" is used), the header help blog generator like hugo to generate html correctly.

just run

```bash
python3 pipeline.py -f YorMarkdown.md -t YourTime
```
Then, a new floder which use the same name as "YorMarkdown.md" will be created and pics in "YorMarkdown.md" will be downloaded into it. "YorMarkdown.md" will be modified using the templete and finally saved as index.md. "YourTime" is the time when "YorMarkdown.md" is writed, YourTime should use YYYY-MM-DD format.