
import win32com.client
olMailItem = 0x0
obj = win32com.client.Dispatch("Outlook.Application")
newMail = obj.CreateItem(olMailItem)
newMail.Subject = "My Subject"
newMail.Body = "My Body"
newMail.To  = "charleszhao@hotmail.co.uk"
newMail.Send()