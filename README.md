# Kylie
Kylie is a voice assistant powered by CrewAI agents. Built in Python, it handles everyday OS tasks (via os) and web actions (via Selenium) locally fast, private, and distraction-free. Your invisible co-pilot for files, apps, and the web.

Note: Under Development

## Current Capabilities

Kylie can currently:

#### 1. Search files 🗂️
  - Find files in configured drives using partial or exact names.
  - Returns the path of the first match or a list of matches.

#### 2. Open files 📂
  - Automatically opens files if found after search.
  - Ensures only one search per query and avoids repeating searches.

#### 3. Close running applications ❌
  - Closes applications by process name.

#### 4. Close folders 📁
  - Closes folder windows using close_folder_window.

#### 5. Create files or folders ➕
  - Creates files or folders if the context is sufficient.

#### 6. Delete files or folders 🗑️
  - Deletes files or folders if the context is sufficient.
    
#### 7. List directories and folders 📋
  - Lists the contents of directories or folders.

#### 8. Ask for clarification ❓
  - If the user command lacks enough information, Kylie asks follow-up questions and waits for user input before proceeding.
