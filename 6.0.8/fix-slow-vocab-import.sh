#!/bin/bash -x
# This command fixes slow vocab imports on Dragon 6.0.8. Don’t try this on other Dragon versions, as it might break something.
sudo /usr/libexec/PlistBuddy -c 'Set :$objects:227:NSAutomaticallyRearrangesObjects false' -c 'Set :$objects:631:NSAutomaticallyRearrangesObjects false' /Applications/Dragon.app/Contents/Resources/Base.lproj/VocabularyEditor.nib
