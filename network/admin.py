from django.contrib import admin
from network.models import Content, Node, Connection, Share

""" Inlines """
    
class SenderInline(admin.TabularInline):
    model = Connection
    fk_name = 'sender'

class ReceiverInline(admin.TabularInline):
    model = Connection
    fk_name = 'receiver'

class ShareInline(admin.TabularInline):
    model = Share
    fk_name = 'user'
    
class ContentInline(admin.TabularInline):
    model = Node.sharedcontent.through
    extra = 3

""" Admins """

class NodeAdmin(admin.ModelAdmin):
    #~ fields = ['name', 'email']       # affects edit page
    #~ list_display = ('name', 'email')    # affects change list page
    inlines = [SenderInline,ReceiverInline,ShareInline]
    #~ search_fields = ('name', 'email')
    
class ContentAdmin(admin.ModelAdmin):
    inlines = [ContentInline]
    search_fields = ('url',)

#~ class ShareAdmin(admin.ModelAdmin):
    #~ list_display = ('__unicode__','timestamp',)
    #~ list_filter = ('timestamp',)

admin.site.register(Node, NodeAdmin)
admin.site.register(Connection)
admin.site.register(Share)
admin.site.register(Content, ContentAdmin)
