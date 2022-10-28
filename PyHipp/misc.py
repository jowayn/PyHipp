def getChannelInArray(channel_name, fig):
    rows = 5
    cols = 8
    channel_num = int(channel_name[-3:])
    if channel_num < 7:
        spind = 8 - channel_num
    elif channel_num < 15:
        spind = 23 - channel_num
    elif channel_num < 23:
        spind = 39 - channel_num
    elif channel_num < 31:
        spind = 55 - channel_num
    elif channel_num < 33:
        spind = 71 - channel_num
    elif channel_num < 39:
        spind = 39 - channel_num
    elif channel_num < 47:
        spind = 55 - channel_num
    elif channel_num < 55:
        spind = 71 - channel_num
    elif channel_num < 63:
        spind = 87 - channel_num
    elif channel_num < 65:
        spind = 103 - channel_num
    elif channel_num < 71:
        spind = 71 - channel_num
    elif channel_num < 79:
        spind = 87 - channel_num
    elif channel_num < 87:
        spind = 103 - channel_num
    elif channel_num < 95:
        spind = 119 - channel_num
    elif channel_num < 97:
        spind = 135 - channel_num
    elif channel_num < 103:
        spind = 103 - channel_num
    elif channel_num < 111:
        spind = 119 - channel_num
    elif channel_num < 119:
        spind = 135 - channel_num
    elif channel_num < 125:
        spind = 150 - channel_num

    # check if it is the corner subplot so we can add ticks and labels
    isCorner = 0
    if channel_num < 33:
        if spind == 2:
            isCorner = 1
    else:
        if spind == 1:
            isCorner = 1
            
    return fig.add_subplot(rows, cols, spind), isCorner
