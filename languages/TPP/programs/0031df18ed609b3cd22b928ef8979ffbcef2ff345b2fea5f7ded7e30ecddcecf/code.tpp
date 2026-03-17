--##
--## sysinfo.tpp - System Information Presentation
--## Demonstrates TPP (Text Presentation Program) features
--##

--title System Information
--author Demo User
--date today
--bgcolor black
--color white

--newpage
--heading Hostname
--exec hostname
--pause

--newpage
--heading Operating System
--exec uname -a
--pause

--newpage
--heading Disk Usage
--exec df -h /
--pause

--newpage
--heading Memory
--exec free -h
--pause

--newpage
--heading Summary
--color cyan
--center All done!
--color white
--bold Thank you for using TPP.
