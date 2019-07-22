from common.do_config import config
class GetApprover:
    def getapprover(self):
        data1=config.get("edit_ap","groupoption")
        approvers=eval(data1)["approvalUserOptions"]
        data2=config.get("edit_ap","categoryoption")
        options=eval(data2)["approvalFlowOptions"]
        print(type(options[0]))
        n = 1
        for i in options:
            m = 1
            if i["approvalType"]=="AND":
                for j in approvers:
                    name="approver"+str(m + 10*n)
                    config.set("edit_ap",name,j["cnName"])
                    m += 1
                    print(j["cnName"])
            else:
                for j in approvers:
                    name = "approver" + str(m + 10*n)
                    config.set("edit_ap", name, j["cnName"])
                    break

            n+=1

