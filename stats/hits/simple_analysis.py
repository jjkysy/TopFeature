import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Function to plot Line Plot with Shaded Area
def plot_line_shaded(ax, diff_before, diff_after):
    smooth_factor = 30
    mean_diff_before = np.mean(diff_before, axis=0)
    std_diff_before = np.std(diff_before, axis=0)
    mean_diff_after = np.mean(diff_after, axis=0)
    std_diff_after = np.std(diff_after, axis=0)
    mean_diff_before_smooth = np.convolve(mean_diff_before, np.ones(smooth_factor)/smooth_factor, mode='valid')
    std_diff_before_smooth = np.convolve(std_diff_before, np.ones(smooth_factor)/smooth_factor, mode='valid')
    mean_diff_after_smooth = np.convolve(mean_diff_after, np.ones(smooth_factor)/smooth_factor, mode='valid')
    std_diff_after_smooth = np.convolve(std_diff_after, np.ones(smooth_factor)/smooth_factor, mode='valid')

    # Calculate and print the average difference between the green and blue lines
    avg_diff = np.mean(mean_diff_after_smooth - mean_diff_before_smooth)
    avg_diff_percentage = (avg_diff / np.mean(mean_diff_before_smooth)) * 100
    print(f'绿色线平均比蓝色线高 {avg_diff_percentage:.2f}%')


    sns.lineplot(x=np.arange(len(mean_diff_before_smooth)), y=mean_diff_before_smooth, 
                 label='Before Optimization', color='blue', errorbar=None, ax=ax)
    ax.fill_between(range(len(mean_diff_before_smooth)), 
                    mean_diff_before_smooth - 0.5 * std_diff_before_smooth, 
                    mean_diff_before_smooth + 0.5 * std_diff_before_smooth, 
                    color='blue', alpha=0.2)
    
    sns.lineplot(x=np.arange(len(mean_diff_after_smooth)), y=mean_diff_after_smooth, 
                 label='After Optimization', color='green', errorbar=None, ax=ax)
    ax.fill_between(range(len(mean_diff_after_smooth)), 
                    mean_diff_after_smooth - 0.5 * std_diff_after_smooth, 
                    mean_diff_after_smooth + 0.5 * std_diff_after_smooth, 
                    color='green', alpha=0.2)

    # sns.lineplot(x=np.arange(mean_diff_before.shape[0]), y=mean_diff_before, 
    #              label='Before Optimization', color='blue', errorbar=None, ax=ax)
    # ax.fill_between(range(mean_diff_before.shape[0]), 
    #                 mean_diff_before - std_diff_before, 
    #                 mean_diff_before + std_diff_before, 
    #                 color='blue', alpha=0.2)
    # sns.lineplot(x=np.arange(mean_diff_after.shape[0]), y=mean_diff_after, 
    #              label='After Optimization', color='green', errorbar=None, ax=ax)
    # ax.fill_between(range(mean_diff_after.shape[0]), 
    #                 mean_diff_after - std_diff_after, 
    #                 mean_diff_after + std_diff_after, 
    #                 color='green', alpha=0.2)

    ax.set_title('Comparison of Cumulative Hits Before and After Optimization', fontsize=26)
    ax.set_xlabel('Steps', fontsize=26)
    ax.set_ylabel('Difference in Cumulative Hits', fontsize=26)
    ax.legend()
    ax.grid(True)

# Function to plot Box Plot
def plot_box(ax, diff_before, diff_after):
    sns.boxplot(data=[diff_before.flatten(), diff_after.flatten()], 
                palette=["blue", "green"], ax=ax)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Before Optimization', 'After Optimization'], fontsize=26)
    ax.set_title('Box Plot of Cumulative Hits Difference Before and After Optimization', fontsize=26)
    ax.set_ylabel('Difference in Cumulative Hits', fontsize=26)
    ax.grid(True)

# Function to plot Paired Bar Plot
def plot_paired_bar(ax, diff_before, diff_after, time_step=1999, labels=None):
    before_data = diff_before[:, time_step]
    after_data = diff_after[:, time_step]
    
    # If no labels provided, create default labels based on the number of groups
    if labels is None:
        labels = [f'Group {i+1}' for i in range(diff_before.shape[0])]
    
    x = np.arange(len(labels))
    width = 0.8 / len(labels)  # Adjust the width based on the number of groups

    rects1 = ax.bar(x - width/2, before_data, width, label='Before Optimization', color='blue')
    rects2 = ax.bar(x + width/2, after_data, width, label='After Optimization', color='green')
    
    ax.set_xlabel('Groups')
    ax.set_ylabel('Cumulative Hits Difference')
    ax.set_title('Paired Bar Plot of Cumulative Hits Difference Before and After Optimization')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Annotate the bars with their heights
    for rect in rects1 + rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), 
                    textcoords="offset points",
                    ha='center', va='bottom')
    plt.tight_layout()


# Function to plot Area Plot
def plot_area(ax, diff_before, diff_after, time_steps):
    sns.set_theme(style="whitegrid")
    ax.fill_between(time_steps, diff_before.mean(axis=0), alpha=0.5, color='blue', label='Before Optimization')
    ax.fill_between(time_steps, diff_after.mean(axis=0), alpha=0.5, color='green', label='After Optimization')
    ax.set_title('Area Plot of Cumulative Hits Difference Before and After Optimization')
    ax.set_xlabel('Time Steps')
    ax.set_ylabel('Average Difference in Cumulative Hits')
    ax.legend()

# Main function to plot all figures in a 2x2 grid
def plot_all_figures(save_path, save_name):
    # Create a 2x2 grid for displaying all four plots
    fig, axs = plt.subplots(2, 2, figsize=(20, 12))
    # Plot all four figures
    plot_line_shaded(axs[0, 0], diff_before, diff_after)
    axs[0, 0].legend(fontsize=20)  # Increase legend font size
    axs[0, 0].set_title('Comparison of Cumulative Hits Before and After Optimization', fontsize=20)  # Increase title font size
    axs[0, 0].set_xlabel('Steps', fontsize=20)  # Increase x-axis label font size
    axs[0, 0].set_ylabel('Difference in Cumulative Hits', fontsize=20)  # Increase y-axis label font size
    
    plot_box(axs[0, 1], diff_before, diff_after)
    axs[0, 1].set_title('Box Plot of Cumulative Hits Difference Before and After Optimization', fontsize=20)  # Increase title font size
    axs[0, 1].set_ylabel('Difference in Cumulative Hits', fontsize=20)  # Increase y-axis label font size
    
    plot_paired_bar(axs[1, 0], diff_before, diff_after)
    axs[1, 0].set_title('Paired Bar Plot of Cumulative Hits Difference Before and After Optimization', fontsize=20)  # Increase title font size
    axs[1, 0].set_xlabel('Groups', fontsize=20)  # Increase x-axis label font size
    axs[1, 0].set_ylabel('Cumulative Hits Difference', fontsize=20)  # Increase y-axis label font size
    
    plot_area(axs[1, 1], diff_before, diff_after, time_steps)
    axs[1, 1].set_title('Area Plot of Cumulative Hits Difference Before and After Optimization', fontsize=20)  # Increase title font size
    axs[1, 1].set_xlabel('Time Steps', fontsize=20)  # Increase x-axis label font size
    axs[1, 1].set_ylabel('Average Difference in Cumulative Hits', fontsize=20)  # Increase y-axis label font size
    
    # Adjust layout for better spacing
    plt.tight_layout()
    # Show the full 2x2 grid of plots
    plt.show()
    
    # Create a new figure for saving only the first two plots in a 1x2 grid
    fig_save, axs_save = plt.subplots(1, 2, figsize=(30, 10))
    # Plot the first two figures in the new 1x2 grid
    plot_line_shaded(axs_save[0], diff_before, diff_after)
    axs_save[0].legend(fontsize=34)  # Increase legend font size
    axs_save[0].set_title('Comparison of Hits per Step (N = 200, e = 5)', fontsize=34)  # Increase title font size
    axs_save[0].set_xlabel('Steps', fontsize=34)  # Increase x-axis label font size
    axs_save[0].set_ylabel('Difference in Cumulative Hits', fontsize=34)  # Increase y-axis label font size

    plot_box(axs_save[1], diff_before, diff_after)
    axs_save[1].set_title('Box Plot of Hits Difference per Step (N = 200, e = 5)', fontsize=34)  # Increase title font size
    axs_save[1].set_ylabel('Difference in Cumulative Hits', fontsize=34)  # Increase y-axis label font size
    
    # Adjust layout for better spacing
    plt.tight_layout()
    # Save the new figure with the first two plots
    plt.savefig(save_path + save_name)
    # Close the figures to free up memory
    plt.close(fig)
    plt.close(fig_save)

# Data loading and preparation (place this at the top)
data_path = "stats/hits/"
file_name = ["cumulative_hits_over_time_50.npy", "cumulative_hits_over_time_100.npy", "cumulative_hits_over_time_200.npy", "cumulative_hits_over_time_300.npy"]
optimized_file_name = ["optimized_cumulative_hits_over_time_50.npy", "optimized_cumulative_hits_over_time_100.npy", "optimized_cumulative_hits_over_time_200.npy", "optimized_cumulative_hits_over_time_300.npy"]

load_data_index = 3
cumulative_hits_before = np.load(data_path + file_name[load_data_index])
cumulative_hits_after = np.load(data_path + optimized_file_name[load_data_index])

diff_before = cumulative_hits_before[1:] - cumulative_hits_before[0]
diff_after = cumulative_hits_after[1:] - cumulative_hits_after[0]

# 只取最后两个数据
diff_before = diff_before[-2:]
diff_after = diff_after[-2:]

time_steps = np.arange(cumulative_hits_before.shape[1])

# Call the main function to plot and save the combined figures
save_path = "plots/optimized_plots/"
plot_all_figures(save_path, "combined_figures_" + file_name[load_data_index].split('_')[-1].split('.')[0] + ".png")
