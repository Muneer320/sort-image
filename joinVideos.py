from moviepy.editor import VideoFileClip, clips_array, ColorClip
import cv2
import os
from rich import print

def add_text_cv2(clip, text):
    """Add text to clip using OpenCV instead of ImageMagick"""
    
    def _add_text_frame(frame, txt):
        # Convert frame to OpenCV format (BGR)
        img = frame.copy()
        
        # Create semi-transparent overlay for text background
        h, w = img.shape[:2]
        overlay = img.copy()
        cv2.rectangle(overlay, (0, h-40), (w, h), (0, 0, 0), -1)
        
        # Add text to the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        font_thickness = 2
        text_size = cv2.getTextSize(txt, font, font_scale, font_thickness)[0]
        text_x = (w - text_size[0]) // 2
        text_y = h - 15  # Position text within the overlay
        
        cv2.putText(overlay, txt, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)
        
        # Blend overlay with original frame
        alpha = 0.7
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
        
        return img
    
    return clip.fl_image(lambda frame: _add_text_frame(frame, text))

def create_video_grid(video_folder, output_filename="output_grid.mp4", grid_size=(2, 3), 
                      target_duration=30):
    """
    Create a grid of videos with text overlays using OpenCV.
    
    Args:
        video_folder: Directory containing input videos
        output_filename: Name of the output file
        grid_size: Tuple (rows, columns) for grid layout
        target_duration: Target duration in seconds for each video
    """
    # Get video files from the folder
    video_files = [f for f in os.listdir(video_folder) if f.lower().endswith(('.mp4')) and "sort" in f]
    print(f"Found {len(video_files)} video files")
    
    # Limit to the needed number of videos based on grid size
    total_videos = grid_size[0] * grid_size[1]
    video_files = video_files[:total_videos]
    
    if len(video_files) < total_videos:
        print(f"Warning: Only found {len(video_files)} videos, but grid needs {total_videos}")
    
    # Load all video clips
    clips = []
    filenames = []
    for f in video_files:
        try:
            clip_path = os.path.join(video_folder, f)
            print(f"Loading: {clip_path}")
            clips.append(VideoFileClip(clip_path))
            filenames.append(f)
        except Exception as e:
            print(f"Error loading {f}: {e}")
    
    # Speed up videos to match target duration instead of trimming
    print(f"Speeding up videos to match {target_duration} seconds duration")
    normalized_clips = []
    for clip in clips:
        if clip.duration <= target_duration:
            # If clip is already shorter than target, keep as is
            normalized_clips.append(clip)
        else:
            # Calculate speed factor to reach target duration
            speed_factor = clip.duration / target_duration
            print(f"Speeding up clip by factor of {speed_factor:.2f}x")
            normalized_clips.append(clip.speedx(speed_factor))
    
    # Output at 1920x1080 resolution
    output_width, output_height = 1920, 1080
    
    # Calculate individual clip sizes
    clip_width = output_width // grid_size[1]
    clip_height = output_height // grid_size[0]
    
    # Resize all clips to the same dimensions while maintaining aspect ratio
    resized_clips = [clip.resize((clip_width, clip_height)) for clip in normalized_clips]
    
    # Add text overlays using OpenCV
    titled_clips = []
    for i, clip in enumerate(resized_clips):
        if i < len(filenames):
            # Convert filename to title case and remove extension
            base_title = os.path.splitext(filenames[i])[0].replace('_', ' ').title()
            speed_factor = clips[i].duration / target_duration
            title = f"{base_title} ({speed_factor:.1f}x)"
            titled_clips.append(add_text_cv2(clip, title))
        else:
            titled_clips.append(clip)
    
    # Arrange clips in grid
    grid = []
    clip_idx = 0
    for i in range(grid_size[0]):
        row = []
        for j in range(grid_size[1]):
            if clip_idx < len(titled_clips):
                row.append(titled_clips[clip_idx])
                clip_idx += 1
            else:
                # Create a blank clip if we run out of videos
                blank = ColorClip((clip_width, clip_height), color=(0, 0, 0))
                blank = blank.set_duration(target_duration)
                row.append(blank)
        grid.append(row)
    
    # Create the grid composition
    final_clip = clips_array(grid)
    
    # Write the final video
    output_path = os.path.join(video_folder, output_filename)
    print(f"Writing video to: {output_path}")
    final_clip.write_videofile(output_path, codec='libx264', threads=4)
    print(f"Video grid created at: {output_path}")

# Example usage
if __name__ == "__main__":
    # Update this path to where your videos are stored
    video_folder = r"d:\Muneer\MainFolder\CodingPractices\Visual Sorting"
    
    create_video_grid(
        video_folder=video_folder,
        output_filename="combined_grid.mp4",
        grid_size=(2, 3),  # 2 rows, 3 columns (3 across, 2 down)
        target_duration=30  # Target duration - videos will be sped up to match
    )