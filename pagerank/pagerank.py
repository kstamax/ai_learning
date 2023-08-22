import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 1000000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    number_of_pages = len(corpus.keys())
    random_page_choice_chance = 1 - damping_factor
    res_trans = {}
    for cor in corpus:
        res_trans[cor] = random_page_choice_chance/number_of_pages + (1/len(corpus[page]) * damping_factor if cor in corpus[page] else 0)
    return res_trans


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    c_page = random.choice(list(corpus.keys()))
    chain = []
    for _ in range(n):
        transition_dict = transition_model(corpus, c_page, damping_factor)
        pages, probs = list(transition_dict.keys()), list(transition_dict.values())
        chain.append(random.choices(pages, weights=probs, k=1)[-1])
        c_page = chain[-1]

    res_dict = {}
    chain_length = len(chain)
    for page in corpus:
        res_dict[page] = len([x for x in chain if x == page])/chain_length
    return res_dict
        


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    damp_random_const = (1-damping_factor)/len(corpus)
    res_dict = {}
    for page in corpus:
        res_dict[page] = 1/len(corpus)
    
    while True:
        next_gen_res_dict = res_dict.copy()
        for page in res_dict:
            prob_sum = sum([1/len(corpus[x]) * res_dict[x] for x in corpus if page in corpus[x]])
            next_gen_res_dict[page] = damp_random_const + prob_sum * damping_factor
        if all([abs(res_dict[page] - next_gen_res_dict[page]) < 0.0001 for page in res_dict]):
            return next_gen_res_dict
        res_dict = next_gen_res_dict.copy()


if __name__ == "__main__":
    main()
