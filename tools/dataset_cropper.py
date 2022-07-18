from math import floor

class Image_Cropper:
    # Returns crops from a given image, always keeping the crops smaller than the given max resolution.
    def __init__(self, max_height, max_width):
        self.max_height = max_height 
        self.max_width = max_width

    def crop(self, img):
        crops = list()
        height,width=img.shape[0:2]

        if width>self.max_width or height>self.max_height:
            print(f'Cropping image...')

            if width<self.max_width*2: tile_w_n=2
            elif width<self.max_width*3: tile_w_n=3
            else: tile_w_n=4
                
            tile_width=floor(width/tile_w_n)

            if height<self.max_height*2: tile_h_n=2
            elif height<self.max_height*3: tile_h_n=3
            else: tile_h_n=4

            tile_height=floor(height/tile_h_n)

            tile_num=tile_w_n*tile_h_n
            
            for index_w in range(tile_w_n):
                for index_h in range(tile_h_n):
                    crop = img[tile_height*index_h:tile_height*(index_h+1),tile_width*index_w:tile_width*(index_w+1)]
                    crops.append(crop)
                    
            print(f'Image cropped in {tile_num} tiles! {tile_w_n}x{tile_h_n}')

        else:
            print(f'Image too small to be cropped')

        return crops,tile_w_n,tile_h_n
        