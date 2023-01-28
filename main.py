from PIL import Image, ImageDraw, ImageFont
import sys
import random

class Coor:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class TextRect:
    word = ""
    freq = 0
    size = Coor(1, 1)
    pos = Coor(1, 1)
    textColor = (200, 200, 200)
    def __init__ (self, word, freq, size):
        self.word = word
        self.freq = freq
        self.size = size
    def draw(self, brush, fontName, fontScale):
        fontScale = fontScale * self.freq
        font = ImageFont.truetype("consola.ttf", fontScale)
        #brush.rectangle([(self.pos.x, self.pos.y), self.pos.x + self.size.x, self.pos.y + self.size.y], 
        #            fill=(20, 20, 20), outline=None, width=1)
        brush.text((self.pos.x, self.pos.y), self.word, font=font, fill=self.textColor)
        
def readFromCSV(fileName):
    data = open(fileName, "r").read().strip("\n\r").split('\n')
    words = []
    for r in data:
        r = r.split(',')
        #print(r)
        words.append((r[0], int(r[1])))
    return words

def createWordRectangles(words, scale):
    wordCloud = []
    for word in words:
        size = Coor(len(word[0]) * scale.x * word[1], scale.y * word[1])
        wordCloud.append(TextRect(word[0], word[1], size))
    return wordCloud

def randomPosWordCloud(wordCloud, imgSize, imgPadding):
    maxAttempts = 1000
    for attempts in range(1, maxAttempts) :
        for word in wordCloud :
            word.pos = Coor(-99999, -99999)
        count = 0
        for word in wordCloud:
            for _ in range(1, maxAttempts) :
                word.pos = Coor(random.randrange(imgPadding.x, imgSize.x - word.size.x - imgPadding.x), 
                                random.randrange(imgPadding.y, imgSize.y - word.size.y - imgPadding.y))
                doesOverlap = False
                for r in wordCloud :
                    if(r is not word and doTextRectanglesOverlapp(r, word)) :
 #                       word.pos = Coor(0, 0)
                        doesOverlap = True
                        break
                if not doesOverlap : break
            if doesOverlap == True : count += 1
                
        if count == 0 :
            print("random pos found for all text rectangles after " + str(attempts) + " attempt(s)")
            return True
    print("random pos not found after " + str(maxAttempts) + " attempts", 
          "\nYou can increase the number of attempts or you can "
          + "adjust image size, padding and font scale settings")
    return False
        
        

def doTextRectanglesOverlapp(a: TextRect, b: TextRect) :
    if (a.pos.x >= b.pos.x + b.size.x or a.pos.y >= b.pos.y + b.size.y) : return False
    if (b.pos.x >= a.pos.x + a.size.x or b.pos.y >= a.pos.y + a.size.y) : return False
    return True
        
def main():
    
    words = readFromCSV("words.csv")
    words.sort(key = lambda x : x[1], reverse=True)
    
    fontName = "Arial.ttf"
    fontScale = 11
    
    wordCloud = createWordRectangles(words, Coor(6, 11))
    imgSize = Coor(1920, 1080)
    img = Image.new('RGB', (imgSize.x, imgSize.y), color = 'black')
    brush = ImageDraw.Draw(img)
    
    randomPosWordCloud(wordCloud, imgSize, Coor(300, 300))
    
    
    for word in wordCloud :
        word.draw(brush, fontName, fontScale)
    
    img.save('output.png')
    
if __name__ == "__main__":
    main()