import unittest
from wiki.core import *


class TestWiki(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wiki = Wiki(os.getcwd())

        for i in range(1, 4):
            f = open(cls.wiki.root + "wiki-test-" + str(i) + ".md", "w")
            f.write("title: Test" + str(i) + "\nmod2: " + str(i % 2) +
                    "tags: exampletag, tag" + str(i) + "\n\n# Test File " + str(i))
            f.close()

    def test_path(self):
        url = "test-markdown-url"
        self.assertTrue(self.wiki.path(url) == os.getcwd() + "test-markdown-url.md")

    def test_exists(self):
        self.assertTrue(self.wiki.exists("wiki-test-1"))

    def test_delete(self):
        f = open(self.wiki.root + "wiki-test-5.md", "w")
        f.write("# Test Move")
        f.close()
        self.assertFalse(self.wiki.exists("wiki-test-5"))

    def test_move(self):
        f = open(self.wiki.root + "wiki-test-5.md", "w")
        f.write("# Test Move")
        f.close()
        self.wiki.move("wiki-test-5", "wiki-test-6")
        self.assertTrue(not self.wiki.exists("wiki-test-5") and self.wiki.exists("wiki-test-6"))

    def test_get(self):
        page = self.wiki.get("wiki-test-1")
        self.assertTrue(page is not None and page.title == "Test1")

    def test_get_bare(self):
        page = self.wiki.get_bare("wiki-test-8")
        self.assertTrue(not self.wiki.get_bare("wiki-test-1") and page)

    def test_index(self):
        pages = self.wiki.index()
        self.assertTrue(len(pages) == 4)

    def test_index_by(self):
        pages = self.wiki.index_by('mod2')
        self.assertTrue(len(pages.get("1")) == len(pages.get("2")) == 2)

    # no need to test get_by_title since it just uses index_by

    def test_get_tags(self):
        tags = self.wiki.get_tags()
        self.assertTrue(len(tags) == 6 and len(tags['exampletag']) == 5 and len(tags['tag1']) == 1)

    def index_by_tag(self):
        exIndex = self.wiki.index_by_tag("examplestag")
        tag1Index = self.wiki.index_by_tag("tag1")
        self.assertTrue(len(exIndex) == 5 and len(tag1Index) == 1 and tag1Index[0].title == "Test1")

    def test_search(self):
        self.assertTrue(len(self.wiki.search("test1")) == 1 and len(self.wiki.search("test")) == 4)

    @classmethod
    def tearDownClass(cls):
        for i in range(1, 4):
            os.remove(os.getcwd() + "wiki-test-" + str(i) + ".md")


class TestWikiPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = []
        for i in range(1, 4):
            s = "wiki-test" + str(i)
            cls.pages.append(Page(s + ".md", s, True))
            f = open(os.getcwd() + "wiki-test-" + str(i) + ".md", "w")
            f.write("title: Test" + str(i) + "\nmod2: " + str(i % 2) + "\n\n# Test File " + str(i))
            f.close()

    def test_load(self):
        self.pages[0].load()
        self.assertTrue(self.pages[0].content and "Test" in self.pages[0].content)

    def test_render(self):
        self.pages[0].load()
        self.pages[0].render()
        self.assertTrue(self.pages[0].body and "<h1>" in self.pages[0].html)

    # tests save() if the .md exists
    def test_save_exists(self):
        f = open(os.getcwd() + "wiki-test-5.md", "w")
        f.write("title: Test5\ntags: \n\n# Test File 5")
        f.close()

        page = Page(os.getcwd() + "wiki-test-5.md", "wiki-test-5")
        page.title("TestEdited")
        page.save()
        if os.path.exists(os.getcwd() + "wiki-test-6.md"):
            f = open(os.getcwd() + "wiki-test-6.md", "r", encoding="utf-8")
            s = f.read()
            f.close()
            os.remove(os.getcwd() + "wiki-test-6.md")
        else:
            s = ""
            os.remove(os.getcwd() + "wiki-test-5.md")
        self.assertTrue("TestEdited" in s and "Test5" not in s)  # making sure there's no appending going on

    def test_save_not_exists(self):
        page = Page(os.getcwd() + "wiki-test-6.md", "wiki-test-6")
        page.title("Test6")
        page.body = "# Test File 6"
        page.save()
        if os.path.exists(os.getcwd() + "wiki-test-6.md"):
            f = open(os.getcwd() + "wiki-test-6.md", "r", encoding="utf-8")
            s = f.read()
            f.close()
            os.remove(os.getcwd() + "wiki-test-6.md")
        else:
            s = ""
            os.remove(os.getcwd() + "wiki-test-5.md")
        self.assertTrue("Test6" in s and "Test File" in s)

    @classmethod
    def tearDownClass(cls):
        for i in range(1, 4):
            os.remove(os.getcwd() + "wiki-test-" + str(i) + ".md")


class TestProcessor(unittest.TestCase):
    # no preprocessors currently
    def test_process_pre(self):
        pass

    def test_process_markdown(self):
        success = True
        for i in range(1, 3):
            md = Processor(("#" * i) + "Test File " + str(i)).process_markdown()
            if not "h" + str(i) in md:
                success = False
        self.assertTrue(success)

    def test_split_raw(self):
        proc = Processor("title: test\ntest: test\ntags: tag1, tag2\n\n# This is a test").split_raw()
        self.assertTrue(proc.meta_raw == "title: test\ntest: test\ntags: tag1, tag2"
                        and proc.markdown == "# This is a test")

    def test_process_meta(self):
        proc = Processor("")
        proc.meta_raw = "title: test\ntest: test\ntags: tag1, tag2"
        proc.process_meta()
        self.assertTrue(proc.meta['title'] == "test" and proc.meta['test'] == 'test'
                        and proc.meta['tags'] == "tag1, tag2")

    def test_process_post(self):
        text = "[[path/name]]"
        proc = Processor("text")
        proc.html = text
        proc.process_post()
        self.assertTrue("<a href=\"path/name\">" in proc.final)


if __name__ == '__main__':
    unittest.main()
