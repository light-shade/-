from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class Verify(object):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.browser = webdriver.Chrome(
            options=options)
        self.browser.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
             {
                "source":
                        """
                            Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                            })
                        """
            }
        )
        self.browser.implicitly_wait(5)
        self.browser.get('https://m.dianping.com/xian/ch10')

    @staticmethod
    def get_track(distance=200):
        track = []
        current = 0
        t = 1
        v = 0
        a = 5
        while current < distance:
            v0 = v
            v = v0 + a * t
            move = v0 * t + a * t * t / 2
            track.append(round(move))
            current += round(move)
        print(sum(track))
        return track

    def __del__(self):
        self.browser.close()

    def run(self):
        slider = self.browser.find_element_by_xpath('//div[@id="yodaBox"]')
        ActionChains(self.browser).click_and_hold(slider).perform()
        track = self.get_track(200)
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        ActionChains(self.browser).release().perform()