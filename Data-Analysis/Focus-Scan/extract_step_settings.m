function [uniqueStepSettings, numericStepSettings, backgroundFiles] = extract_step_settings(pathToDir)
    flist = dir([pathToDir, '*.tiff']);
    pattern = '(neg|pos)(\d+)_'; 
    bgPattern = '(?i)background|bg';
    stepSettings = [];
    backgroundFiles = [];
    
    for i = 1:length(flist)
        filename = flist(i).name;
        if ~isempty(regexp(filename, bgPattern, 'once'))
            if ~ismember(filename, backgroundFiles) % Avoid duplicates
                backgroundFiles{end+1} = filename;
            end
            continue; % Skip further processing for background files
        end
        tokens = regexp(filename, pattern, 'tokens');
        if ~isempty(tokens)
            stepSettings = [stepSettings; {[tokens{1}{1}, tokens{1}{2}]}];
        end
    end
    uniqueStepSettings = unique(stepSettings);
    numericStepSettings = cellfun(@(s) str2double(regexprep(s, 'neg', '-')), uniqueStepSettings);
    [numericStepSettings, idx] = sort(numericStepSettings, 'descend');
    uniqueStepSettings = uniqueStepSettings(idx);
end