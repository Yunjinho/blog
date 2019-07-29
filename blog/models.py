from django.db import models

class Blog(models.Model):
    title=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')
    body=models.TextField()
    #models.xxxField(~~~)
    
    def __str__(self):
        return self.title 
#제목에 썻던 글 나오게 하기 
    def summary(self):
        return self.body[:100]
    #본문에 100글자 제한
    

    #퀘리셋과 메소드 형식
    #모델.퀘리셋(objects).메소드

    