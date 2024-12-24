from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project_Area
        fields = '__all__'
        labels = {
            'name':'Project Name',
            'projectAreaHref': 'Project Area Href',
            'projectAreaAlias': 'Project Area Alias',
        }

class GlobalConfigurationForm(forms.ModelForm):
    class Meta:
        model = Global_Configuration
        fields = '__all__'
        labels = {
            'gc_id': 'Global Configuration ID',
            'project': 'Project Area',
            'title': 'Configuration Title',
            'component_href': 'Component href'
        }
class TestPlanForm(forms.ModelForm):
    class Meta:
        model = Test_Plan
        fields = '__all__'
        labels = {
            'gc_obj_link': 'Link Global Configuration', 
            'title': 'Test Plan Name',
            'tplan_view_id': 'View ID',
            'tplan_query_id': 'Query ID',
        }

class TestSuiteForm(forms.ModelForm):
    class Meta:
        model = Test_Suite
        fields = '__all__'
        labels = {
            'tplan_obj_link': 'Link Test Plan', 
            'title': 'Test Suite Name',
            'tsuite_view_id': 'View ID',
            'tsuite_query_id': 'Query ID',
        }


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = Test_Case
        fields = '__all__'
        labels = {
            'tsuite_obj_link': 'Link Test Suite',
            'title': 'Test Case Name',
            'state': 'State',
            'tcase_view_id': 'View ID',
            'tcase_query_id': 'Query ID',
            'owner': 'Owner',
            'tcase_type': 'Test Type',
            'functionality ': 'Functionality',
            'tsg_Compliant ': 'TSG Compliant',
            'test_category': 'Test Category',
            'implementation_path': 'Implemetation Path',
            'life_cycle_start': 'Life Cycle Start',
            'life_cycle_end': 'Life Cycle End',
        }

class HWVariantForm(forms.ModelForm):
    class Meta:
        model = HW_Variant
        fields = '__all__'
        labels = {
            'global_configuration': 'Global Configuration',
            'HW_Variant_href': 'HW Variant Href',
            'HW_Variant_value': 'HW Variant Value',
        }

class TestEnvironmentConfigurationForm(forms.ModelForm):
    class Meta:
        model = Test_Environment_Configuration
        fields = '__all__'
        labels = {
            'global_configuration': 'Global Configuration',
            'Test_Environment_Configuration_href': 'Test Environment Configuration Href',
            'Test_Environment_Configuration_name': 'Test Environment Configuration Name',
        }

class TestResultForm(forms.ModelForm):
    class Meta:
        model = Test_Result
        fields = '__all__'
        labels = {
            'project': 'Project',
            'result_state': 'Result State',
            'state_label': 'State Label',
        }

class SWBuildRQMForm(forms.ModelForm):
    class Meta:
        model = Sw_Build_RQM
        fields = '__all__'
        labels = {
            'global_configuration': 'Global Configuration', 
            'build_href': 'SW Build ALM href', 
            'build_id': 'SW Build ALM id', 
            'build_title': 'SW Build Title',
        }

class HILSetupInline(admin.TabularInline):
    model = HIL_Setup
    extra = 1  # Number of empty forms to display

@admin.register(Project_Area)
class ProjectAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'projectAreaHref', 'projectAreaAlias')
    search_fields = ('name', 'projectAreaHref', 'projectAreaAlias')
    inlines = [HILSetupInline]
    form = ProjectForm

@admin.register(HIL_Setup)
class HILSetupAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'port', 'project')
    search_fields = ('name', 'host', 'project_name')

@admin.register(Global_Configuration)
class GlobalConfigurationAdmin(admin.ModelAdmin):
    list_display = ('gc_id', 'project', 'title', 'component_href')
    search_fields = ('gc_id', 'project__name', 'title', 'component__href')
    fieldsets = [
        (
            'General Information',
            {
                'fields': ['gc_id', 'project', 'title', 'component_href'],  
                'description': 'Basic information about the global configuration.'  
            },
        ),
    ]
    
    form = GlobalConfigurationForm

@admin.register(Test_Plan)
class TestPlanAdmin(admin.ModelAdmin):
    list_display = ('tplan_query_id', 'gc_obj_link', 'title')
    search_fields = ('tplan_query_id', 'gc_obj_link', 'title')
    form = TestPlanForm

@admin.register(Test_Suite)
class TestSuiteAdmin(admin.ModelAdmin):
    list_display = ('tsuite_query_id', 'tplan_obj_link', 'title')
    search_fields = ('tsuite_query_id', 'tplan_obj_link', 'title')
    form = TestSuiteForm

@admin.register(Iteration)
class TestIterationAdmin(admin.ModelAdmin):
    list_display = ('tplan_obj_link', 'test_phase_href', 'test_phase_title')
    search_fields = ('tplan_obj_link', 'test_phase_href', 'test_phase_title')
    # form = TestSuiteForm

@admin.register(Test_Case)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('tcase_query_id', 'tcase_view_id', 'tsuite_obj_link', 'title', 'state', 'owner', 'tcase_type', 'functionality', 'tsg_Compliant', 'test_category', 'implementation_path')
    search_fields = ('tcase_query_id', 'tcase_view_id', 'tsuite_obj_link', 'title', 'state', 'owner', 'tcase_type', 'functionality', 'tsg_Compliant', 'test_category', 'implementation_path')
    form = TestCaseForm
@admin.register(HW_Variant)
class HWVariantAdmin(admin.ModelAdmin):
    list_display = ('HW_Variant_value', 'global_configuration')
    search_fields = ('HW_Variant_value', 'global_configuration')
    form = HWVariantForm
 
@admin.register(Test_Environment_Configuration)
class TestEnvironmentConfigurationAdmin(admin.ModelAdmin):
    list_display = ('Test_Environment_Configuration_name', 'global_configuration')
    search_fields = ('Test_Environment_Configuration_name', 'global_configuration')
    form = TestEnvironmentConfigurationForm

@admin.register(Test_Result)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('state_label', 'project')
    search_fields = ('state_label', 'project')
    form = TestResultForm

@admin.register(Sw_Build_RQM)
class SWBuildRQMAdmin(admin.ModelAdmin):
    list_display = ('global_configuration', 'build_href', 'build_id', 'build_title')
    search_fields = ('global_configuration', 'build_href', 'build_id', 'build_title')
    form = TestResultForm
