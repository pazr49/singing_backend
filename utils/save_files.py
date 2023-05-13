def save_files(files):
    if len(files) == 0:
        return 'No file selected', 400

    for index, file in enumerate(files):
        file.save(f'uploaded_video_{index}.mp4')

    return 'Files uploaded successfully'