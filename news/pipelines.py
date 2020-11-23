# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class NewsPipeline:

    # def __init__(self):
    #     self.file = open('news_data.csv', 'wb')
    #     self.exporter = CsvItemExporter(self.file, encoding='utf-8')
    #     self.exporter.start_exporting()
    #
    # def close_spider(self, spider):
    #     self.exporter.finish_exporting()
    #     self.file.close()
    #
    # def process_item(self, item, spider):
    #     self.exporter.export_item(item)
    #     return item

    def __init__(self):
        self.file = open('news_data.txt', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.file.write(item['news_title'])
        self.file.write('\n')
        self.file.write(item['news_time'])
        self.file.write('  ')
        self.file.write('来源：' + item['news_source'])
        self.file.write('\n')
        contents = item['news_body']
        for content in contents:
            self.file.write('   ' + content.replace('\n', '').replace(' ', ''))
            self.file.write('\n')
        self.file.write('*' * 50)
        self.file.write('\n')
        return item
