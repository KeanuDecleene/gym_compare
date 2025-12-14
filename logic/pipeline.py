from address import Address

class gymPipeline():

    def run(self, address):
        """run the pipeline to get gym data from address"""
        coords = Address.find_lat_lon(address)
        




