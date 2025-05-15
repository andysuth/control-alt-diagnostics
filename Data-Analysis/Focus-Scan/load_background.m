function bgData = load_background(pathToDir, backgroundFiles)
    if ~isempty(backgroundFiles)
        bg = Tiff(fullfile(pathToDir, backgroundFiles{1}));
        bgData = double(read(bg));
    else
        bgData = 0;
    end
end