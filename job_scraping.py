# 自动化获取boss招聘网的信息
# 引入By Class，辅助元素定位
# 参考：https://blog.csdn.net/qq_51431069/article/details/138142078

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
import undetected_chromedriver as uc
import random

# 搜索中需要跳过的几种学历
level = ['学历不限', '高中', '中专', '大专', '初中']
# BOOS招聘网站
url = "https://www.zhipin.com/wuhan/"
# 创建谷歌浏览器
browser = uc.Chrome()
# 打开网页
browser.get(url=url)
browser.set_window_size(920, 480)  # 改变页面大小
# 等待10秒钟，最好别访问太快
sleep(10)
# 选择搜索框
searching = browser.find_element(By.XPATH,
                                 '//input[@type="text" and @name="query" and @class="ipt-search" and @placeholder="搜索职位、公司"]')
# 输入，搜素
searching.send_keys("迈瑞医疗")
# 存低学历的num
low_result = []
# 点击搜索，通过回车点击
searching.send_keys(Keys.ENTER)
# 等待10秒
sleep(10)
# 获取表格数据
# 定义一个变量来判断循环的次数
loop_count = 0
# 定义一个空数组，后面用来存储数据
pd_lis = []
# 定义循环持续条件
not_last_page = True
while not_last_page:
    job_list_box = f'//div[@class="search-job-result"]/ul[@class="job-list-box"]'
    job_list_box_li = browser.find_element(By.XPATH, job_list_box)
    li_num = job_list_box_li.find_elements(By.CSS_SELECTOR, 'li.job-card-wrapper')
    # li_num = job_list_box_li.find_elements(By.TAG_NAME, 'li')
    total = len(li_num)
    print('total:', total)

    for num in range(30*loop_count+1, 30*loop_count+total+1):
        # 定位到岗位信息所在的li标签，通过num变量来确认获取哪一行的岗位信息  (搜索页完成）
        li = job_list_box_li.find_element(By.XPATH,
                                          f'//div[@class="search-job-result"]/ul[@class="job-list-box"]/li[@ka="search_list_{num}"]')
        # 指定职位等信息
        div_1 = li.find_element(By.XPATH,
                                f'//div[@class="search-job-result"]/ul[@class="job-list-box"]/li[@ka="search_list_{num}"]/div[@class="job-card-body clearfix"]/a')
        # 获取职位
        job_title = div_1.find_element(By.XPATH,
                                       f'//div[@class="search-job-result"]/ul[@class="job-list-box"]/li[@ka="search_list_{num}"]/div[@class="job-card-body clearfix"]/a/div[@class="job-title clearfix"]/span[@class="job-name"]').text
        # 获取公司位置
        job_address = div_1.find_element(By.XPATH,
                                         f'//div[@class="search-job-result"]/ul[@class="job-list-box"]/li[@ka="search_list_{num}"]/div[@class="job-card-body clearfix"]/a/div[@class="job-title clearfix"]/span[@class="job-area-wrapper"]/span[@class="job-area"]').text
        # 获取薪资
        salary = div_1.find_element(By.XPATH,
                                    f'//div[@class="search-job-result"]/ul[@class="job-list-box"]/li[@ka="search_list_{num}"]/div[@class="job-card-body clearfix"]/a/div[@class="job-info clearfix"]/span[@class="salary"]').text
        # 确认工作经验所属位置
        work_experience = div_1.find_element(By.XPATH,
                                             f'//div[@class="search-job-result"]/ul[@class="job-list-box"]/li[@ka="search_list_{num}"]/div[@class="job-card-body clearfix"]/a/div[@class="job-info clearfix"]/ul[@class="tag-list"]')
        # 获取学历和工作经验
        work_experience_lis = work_experience.find_elements(By.TAG_NAME, 'li')
        # 定义一个变量，用来拼接学历和工作经验，因为有的公司有两个信息，有的公司有三个信息，有的公司没有信息
        work_experience = ""
        for we_li in work_experience_lis:
            work_experience = work_experience + we_li.text if work_experience == "" else work_experience + '/' + we_li.text

        # 获取招聘人员加招聘人员职位
        recruiter_position = div_1.find_element(By.XPATH,
                                                f'//div[@class="search-job-result"]/ul[@class="job-list-box"]/li[@ka="search_list_{num}"]/div[@class="job-card-body clearfix"]/a/div[@class="job-info clearfix"]/div[@class="info-public"]').text
        # 获取招聘人员职位
        position = div_1.find_element(By.XPATH,
                                      f'//div[@class="search-job-result"]/ul[@class="job-list-box"]/li[@ka="search_list_{num}"]/div[@class="job-card-body clearfix"]/a/div[@class="job-info clearfix"]/div[@class="info-public"]/em').text
        # 将招聘人员加招聘人员职位中剔除招聘人员职位,直接替换成空
        recruiter = recruiter_position.replace(position, "")

        # 指定公司信息
        div_2 = li.find_element(By.XPATH,
                                f'//div[@class="search-job-result"]/ul[@class="job-list-box"]/li[@ka="search_list_{num}"]/div[@class="job-card-body clearfix"]/div[@class="job-card-right"]/div[@class="company-info"]')
        # 公司名称
        company_name = div_2.find_element(By.TAG_NAME, 'h3').text
        # 获取公司类型/融资情况/人员规模
        company_type_ul = div_2.find_element(By.XPATH,
                                             f'//div[@class="search-job-result"]/ul[@class="job-list-box"]/li[@ka="search_list_{num}"]/div[@class="job-card-body clearfix"]/div[@class="job-card-right"]/div[@class="company-info"]/ul[@class="company-tag-list"]')
        company_type_lis = company_type_ul.find_elements(By.TAG_NAME, 'li')
        company_join = ""
        for company in company_type_lis:
            # 获取公司类型/融资情况/人员规模
            company_join = company_join + company.text if company_join == "" else company_join + '/' + company.text

        # 获取公司对职位的要求ul标签
        company_requirements_ul = li.find_element(By.XPATH,
                                                  f'//div[@class="search-job-result"]/ul[@class="job-list-box"]/li[@ka="search_list_{num}"]//div[@class="job-card-footer clearfix"]/ul[@class="tag-list"]')
        # 获取公司对职位的要求li标签
        company_requirements_lis = company_requirements_ul.find_elements(By.TAG_NAME, "li")
        company_requirements = ""
        for company_requirements_li in company_requirements_lis:
            # 公司对职位的要求
            company_requirements = company_requirements + company_requirements_li.text if company_requirements == "" else company_requirements + '/' + company_requirements_li.text
        # 获取公司福利
        company_benefits = li.find_element(By.XPATH,
                                           f'//div[@class="search-job-result"]/ul[@class="job-list-box"]/li[@ka="search_list_{num}"]//div[@class="job-card-footer clearfix"]/div').text
        '''
        job_title 职位 - 
        job_address 公司位置
        salary 薪资 - 
        work_experience 学历工作经验
        recruiter 招聘人
        position 招聘人所属职位
        company_name 公司名称
        company_join 公司类型/融资情况/人员规模
        company_requirements 公司要求
        company_benefits 公司福利
        '''

        # 不保存低学历结果
        if not any(edu_level in work_experience for edu_level in level):
            print(num)
            pd_lis.append(
                [company_name, job_title, salary, job_address, work_experience, recruiter, position, company_join,
                 company_requirements, company_benefits])
        else:
            print('低学历', num)
            low_result.append(num)

        if num % 30 == total % 30:
            print('num == total')
            # 获取a标签下最后一个a标签，那个就是点击下一页
            page = browser.find_elements(By.XPATH, '//div[@class="options-pages"]/a')
            last_page = page[-1]
            if 'disabled' in last_page.get_attribute('class'):
                not_last_page = False  # 结束所有循环
                print('最后一页')
                df = pd.DataFrame(data=pd_lis,
                                  columns=['公司名称', '招聘职位', '薪资区间', '公司位置', '要求的学历/工作经验',
                                           '招聘人',
                                           '招聘人所属职位',
                                           '公司类型/融资情况/人员规模', '公司要求', '公司福利'])
                with pd.ExcelWriter('E:/boss_zhipin/test.xlsx', mode='a', engine='openpyxl',
                                    if_sheet_exists="overlay") as writer:
                    df.to_excel(writer, index=False, sheet_name='mairui')
                browser.close()
                browser.quit()
                break
            else:
                # 点击下一页
                last_page.click()

        sleep(random.randint(1, 15))

    loop_count += 1

print('low result:', low_result)
print('finish')
