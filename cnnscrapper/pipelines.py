# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from datetime import datetime

class CnnscrapperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Format date field
        if 'date' in adapter:
            # Remove the "updated " prefix
            date_str = adapter['date']

            # Parse the datetime string
            try:
                # Correct the format string to match "Tue Jul 10 2012 15:52:45"
                adapter['date'] = datetime.strptime(date_str, '%a %b %d %Y %H:%M:%S').date()
            except ValueError as e:
                spider.logger.error(f"Date conversion error for item {adapter['date']}: {e}")
                adapter['date'] = None  # Fallback: could log this or keep the original string

        return item
