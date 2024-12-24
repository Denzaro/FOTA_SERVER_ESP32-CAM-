from django.db import models

# Create your models here.
class Project_Area(models.Model):
    name = models.TextField(primary_key=True)
    projectAreaHref = models.TextField(default="")
    projectAreaAlias = models.TextField(default="")
    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

class HIL_Setup(models.Model):
    project = models.ForeignKey(Project_Area, on_delete=models.CASCADE)
    name = models.TextField(default="")
    href = models.TextField(default="")
    host = models.TextField(default="")
    port = models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "HIL Setup"
        verbose_name_plural = "HIL Setups"
        constraints = [
            models.UniqueConstraint(fields=['project', 'name'], name='unique_field_testsetup')
        ]

class Global_Configuration(models.Model):
    project = models.ForeignKey(Project_Area, on_delete=models.CASCADE)
    title = models.TextField(default="")
    gc_id = models.TextField(default="",primary_key=True)
    component_href = models.TextField(default="")
    
    class Meta:
        verbose_name = "Global Configuration"
        verbose_name_plural = "Global Configurations"

class Test_Plan(models.Model):
    gc_obj_link = models.ForeignKey(Global_Configuration, on_delete=models.CASCADE,related_name='testplan')
    title = models.TextField(default="")
    tplan_view_id = models.TextField(default="")
    tplan_query_id = models.TextField(default="")
    
    def __str__(self):
        return f"{self.title}"
    class Meta:
        verbose_name = "Test Plan"
        verbose_name_plural = "Test Plans"
        constraints = [
            models.UniqueConstraint(fields=['gc_obj_link', 'tplan_query_id'], name='unique_field_testplan')
        ]

class Iteration(models.Model):
    tplan_obj_link = models.ForeignKey(Test_Plan, on_delete=models.CASCADE, related_name='iterations')
    test_phase_href = models.TextField(default="")
    test_phase_title = models.TextField(default="")
	
class Test_Suite(models.Model):
    tplan_obj_link = models.ForeignKey(Test_Plan, on_delete=models.CASCADE,related_name='testsuite')
    title = models.TextField(default="")
    tsuite_view_id = models.TextField(default="")
    tsuite_query_id = models.TextField(default="")

    def __str__(self):
        return f"{self.title}"
    class Meta:
        verbose_name = "Test Suite"
        verbose_name_plural = "Test Suites"
        constraints = [
            models.UniqueConstraint(fields=['tplan_obj_link', 'tsuite_query_id'], name='unique_field_testsuite')
        ]

class Test_Case(models.Model):
    tsuite_obj_link = models.ForeignKey(Test_Suite, on_delete=models.CASCADE,related_name='testcase')
    title = models.TextField(default="")
    state = models.CharField(default="",max_length=255)
    tcase_view_id = models.TextField(default="")
    tcase_query_id = models.TextField(default="")
    owner = models.CharField(default="",max_length=255)
    tcase_type = models.CharField(default="",max_length=255)
    functionality = models.CharField(default="",max_length=255)
    tsg_Compliant = models.CharField(default="",max_length=255)
    test_category = models.CharField(default="",max_length=255)
    implementation_path = models.TextField(default="",max_length=255)
    life_cycle_start = models.TextField(default="",max_length=255)
    life_cycle_end = models.TextField(default="",max_length=255)

    def __str__(self):
        return f"{self.title}"
    class Meta:
        verbose_name = "Test Case"
        verbose_name_plural = "Test Cases"
        constraints = [
            models.UniqueConstraint(fields=['tsuite_obj_link', 'tcase_query_id'], name='unique_field_testcases')
        ]
		
class Sw_Build_RQM(models.Model):
    global_configuration = models.ForeignKey(Global_Configuration, on_delete=models.CASCADE)
    build_href = models.TextField(default="")
    build_id = models.TextField(default="")
    build_title = models.TextField(default="")
    def __str__(self):
        return f"{self.build_title}"
    
class HW_Variant(models.Model):
    global_configuration = models.ForeignKey(Global_Configuration, on_delete=models.CASCADE)
    HW_Variant_href = models.TextField(default="")
    HW_Variant_value = models.TextField(default="")

    def __str__(self):
        return f"{self.HW_Variant_value}"

class Test_Environment_Configuration(models.Model):
    global_configuration = models.ForeignKey(Global_Configuration, on_delete=models.CASCADE)
    Test_Environment_Configuration_href = models.CharField(default="",max_length=255)
    Test_Environment_Configuration_name =  models.CharField(default="",max_length=255)

    def __str__(self):
        return f"{self.Test_Environment_Configuration_name}"

class Test_Result(models.Model):
    project = models.ForeignKey(Project_Area, on_delete=models.CASCADE)
    result_state = models.TextField(default="")
    state_label = models.TextField(default="")

    def __str__(self):
        return f"{self.result_state}"
