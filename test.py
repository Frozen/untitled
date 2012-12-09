from replace import celery

@celery.task(name='blog.mail_comments_answer_reply')
def my_func_name(id):
    print id


#func_name.a = lambda x : x*5

my_func_name.apply_async(args=(1,))




