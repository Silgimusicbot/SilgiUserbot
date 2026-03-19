    ytaudio = { 'format': 'ba/b', ... }  # Change ytaudio ydl_opts format
    # other existing lines

    extractor_args = {'youtube': {'player_client': ['web']}}  # Change extractor_args youtube player_client
    # other existing lines

    ytvideo = { 'format': 'bv*+ba/b', ... }  # Change ytvideo ydl_opts format
    # other existing lines

    try:
        # existing code
    except Exception as e:
        if 'Requested format is not available' in str(e):
            # existing exception handling
            print('Başqa bir bağlantı ya da axtarış etməyə çalışın.');  # Append Azerbaijani hint
