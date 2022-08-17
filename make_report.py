class samreport():
    def __init__(self, report_file):
        self.report_file = report_file
     
    # create report file
    def raw_alert(self, alert):
        with open(self.report_file, "a") as f:
            f.write(alert + "\n")
            f.close()
            print("alert stored")


