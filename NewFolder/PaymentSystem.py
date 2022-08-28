from lib2to3.pgen2.token import BACKQUOTE
from operator import itemgetter
from backend import BackEnd
import datetime

class PaymentSystem:
    
    def __init__(self) -> None:
        self.revPercentage = 40
        self.revIncomeProvidePercentage = 60
        pass

    def CalculateTotalViews(self, users=[])->list:
        for user in users:
            total_views  = user["total_blog_view"]+user["total_views"]
            user["total_views_both"] = total_views
            if "balance" not in user.keys():
                user["balance"] = 0
        return users
    
    def SortUserByViews(self, users=[])->list:
        sortedList = sorted(users, key=itemgetter("total_views_both"), reverse=True)
        return sortedList
    
    def RevenuePercentageCalculate(self):
        pass
        
    def ViewsPercentageCalculate(self, users=[], views_round_to=0):
        total = sum([x["total_views_both"] for x in users])
        for i in users:
            i["views_percentage"] = round((i["total_views_both"] * 100)/total, views_round_to)
        return users   
    
    def getRevenueOfUser(self, users=[], total_revenue=0, amount_round_to=0):
        val = []
        for i in users:
            i["income_this_month"] = round(total_revenue * (i["views_percentage"]/100), amount_round_to)
            val.append(total_revenue * (i["views_percentage"]/100))
        return users       
    
    def getRevenueByPercentageForMembers(self, total_revenue=0):
        return  total_revenue * (self.revIncomeProvidePercentage/100)
        
    def getfinal(self, users, payment):
        t = self.CalculateTotalViews(users=users)
        s = self.SortUserByViews(t) 
        x = self.ViewsPercentageCalculate(s, views_round_to=2)
        z = self.getRevenueOfUser(x, total_revenue=PaymentSystem().getRevenueByPercentageForMembers(total_revenue=payment), amount_round_to=2)
        return z
    
    def getincomebyuserid(self, user_id):
        for i in self.getfinal(users=BackEnd().get_users()):
            if i["user_id"] == user_id:
                return str(i["income_this_month"])
        return False 

    def update_user_income(self):
      payment_1 = int(input("Enter amount :"))
      payment_2 = int(input("Enter amount again :")) 
      if payment_1 == payment_2:        
        week_no = str(datetime.datetime.now().isocalendar()[1])
        week_val = None
        if int(week_no) % 2 == 0: 
                week_val = "e"
        else:
                week_val = "o"
        for i in self.getfinal(users=BackEnd().get_users(), payment=payment_2):
            total_earning = round(i["total_earning"], 2)
            income_this_week = i["income_this_month"]
            balance = round(i["balance"], 2)
            print("income_this_week", income_this_week)
            print("balance",balance)
            print("total_earning",total_earning)
            BackEnd().update_user_incomes(user_id=i["user_id"],
                                          income_this_week=income_this_week,
                                          total_earning=total_earning,
                                          balance=balance
                                          )
        BackEnd().insert_payment_time(week_no=week_no, week_val=week_val)
        return True    
        
    def calculate_page_post_percentage(self, pages, overall_posts):
        for i in pages:
            i["post_perc"] = (i["total_posts"]*100)/overall_posts
        print(pages)    
        return pages
        
    def calculate_income_from_page(self, pages, revenue):
        for i in pages:
            i["income"] = (revenue * (i["post_perc"]/100))  
        print(pages)  
        return pages
# week_val_no = BackEnd().last_payment_document()["week_no"]
# week_no = str(datetime.datetime.now().isocalendar()[1])
# print(week_no)
# print(week_val_no)
# print(type(week_no))
# print(type(week_val_no))
# week_val = None 
# if week_val_no == week_no:
#   print("updated already")
# else:
#     PaymentSystem().update_user_income()


i = PaymentSystem().calculate_page_post_percentage(pages=BackEnd().get_page_total_posts(), overall_posts = len(BackEnd().get_all_opis()))
i_ = PaymentSystem().calculate_income_from_page(pages=i, revenue=70)

