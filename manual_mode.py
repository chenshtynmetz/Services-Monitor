import platform

INDEX_SECONDS = 18
INDEX_MIN = 15
INDEX_HOURS = 12
PID_START_W = 26
PID_END_W = 33
PID_START_L = 8
PID_END_L = 16


class Manual:
    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        self.serviceList = "serviceList.txt"
        try:
            with open(self.serviceList, "r") as f:  # get the time between measures
                time1 = f.readline()
                time_line = time1.split("\n")
                self.my_time = float(time_line[0])
        except IOError:
            self.my_time = 0
        self.system = platform.system()
        self.results = ""

    def monitoring(self):
        if self.my_time == 0:
            self.results += "please activate monitor mode first"
        seconds1 = int(self.time1[INDEX_SECONDS:INDEX_SECONDS + 2]) + int(
            self.time1[INDEX_MIN:INDEX_MIN + 2]) * 60 + int(
            self.time1[INDEX_HOURS:INDEX_HOURS + 2]) * 3600  # get the time in seconds
        seconds2 = int(self.time2[INDEX_SECONDS:INDEX_SECONDS + 2]) + int(
            self.time2[INDEX_MIN:INDEX_MIN + 2]) * 60 + int(self.time2[INDEX_HOURS:INDEX_HOURS + 2]) * 3600
        with open(self.serviceList, "r") as f:
            lines = f.readlines()
        # get the first index of each service list
        first_index_start = self.find_index(seconds1, lines, self.time1)
        second_index_start = self.find_index(seconds2, lines, self.time2)
        if first_index_start == -1 or second_index_start == -1:
            self.results += "can't find time"
            print("can't find time")
            return
        # find the last index of each service list
        first_index_end = lines.index("~\n", first_index_start)
        try:
            second_index_end = lines.index("~\n", second_index_start)
        except ValueError:  # last list in the file
            second_index_end = len(lines) - 1
        first_list = lines[first_index_start + 1:first_index_end]  # take only the relevant lines from the list
        second_list = lines[second_index_start + 1:second_index_end]
        self.results = self.compare(second_list, first_list, self.time1 + " -> " + self.time2)
        print(self.results)

    # find the index of the relevant time in the list
    def find_index(self, seconds, lines, date):
        for i in range(len(lines)):
            if lines[i][0] == "$":
                curr_time = int(lines[i][INDEX_SECONDS:INDEX_SECONDS + 2]) + int(
                    lines[i][INDEX_MIN:INDEX_MIN + 2]) * 60 + int(lines[i][INDEX_HOURS:INDEX_HOURS + 2]) * 3600
                if (seconds - self.my_time) <= curr_time <= (seconds + self.my_time) and lines[i][
                                                                                         :INDEX_HOURS] == date[
                                                                                                          :INDEX_HOURS]:
                    return i
        return -1

    # this function check if something changes
    def compare(self, curr_list, prev_list, curr_time):
        ans = '\n' + curr_time + '\n'
        for i in range(3, len(prev_list)):
            if prev_list[i] not in curr_list:  # services that stopped
                ans += "stopped:" + '\t' + prev_list[i] + '\n'
        for i in range(3, len(curr_list)):
            if curr_list[i] not in prev_list:  # services that started
                ans += "started:" + '\t' + curr_list[i] + '\n'
        return ans
