% Load sound file
[y, Fs] = audioread("midnightRun.m4a");

% Apply filter to sound data
filteredSound = filter(filter1, y);

% Graph the original vs filtered
% time axis
t = (0:length(y) - 1)/Fs;

% plot original
figure;
subplot(2, 1, 1);
plot(t, y);
title("Original");
xlabel("Time (s)");
ylabel("Amplitude");

% plot filtered
subplot(2, 1, 2);
plot(t, filteredSound);
title("Filtered");
xlabel("Time (s)");
ylabel("Amplitude");

% Adjust the plot layout
sgtitle('Comparison of Original and Filtered Sound');