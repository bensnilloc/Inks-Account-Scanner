import re

class Pets:
    def __init__(self, wrapper, functions):
        self.wrapper = wrapper
        self.functions = functions()

    def get_pets(self):
        colour = []
        fishing_skill = []
        jobs_completed = []
        jobs_failed = []
        job_rank = []

        response = self.wrapper.get("island/training.phtml?type=status")
        petnames = re.findall(r"2><b>(.*?) \(Level ", response.text)
        level = re.findall(r"Lvl : <font color=green><b>(.*?)</b></font>", response.text)
        strength = re.findall(r"Str : <b>(.*?)</b><br>", response.text)
        defence = re.findall(r"Def : <b>(.*?)</b><br>", response.text)
        movement = re.findall(r"Mov : <b>(.*?)</b><br>", response.text)
        hp = re.findall(r"Hp  : <b>(.*?)</b><br>", response.text)

        for pet in petnames:
            response = self.wrapper.get(f"petlookup.phtml?pet={pet}")
            _colour = re.findall(r";\">(\w+?) </span>", response.text)
            _fishing_skill = re.findall(r"Fishing Skill:</b> (\d+?)", response.text)
            _jobs_completed = re.findall(r"Jobs Completed:</b> (\d+?)", response.text)
            _jobs_failed = re.findall(r"Jobs Failed:</b> (\d+?)", response.text)
            _job_rank = re.findall(r"Job Rank:</b> (\w+?)\t", response.text)

            for names, clr, fish, jobs_c, jobs_f, job_r in zip(pet, _colour, _fishing_skill, _jobs_completed, _jobs_failed, _job_rank):
                colour.append(clr)
                fishing_skill.append(fish)
                jobs_completed.append(jobs_c)
                jobs_failed.append(jobs_f)
                job_rank.append(job_r)
        
        return petnames, level, strength, defence, movement, hp, colour, fishing_skill, jobs_completed, jobs_failed, job_rank