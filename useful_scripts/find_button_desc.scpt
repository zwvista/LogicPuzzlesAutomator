tell application "100 LG" to activate
delay 3

tell application "System Events"
	tell process "100 LG"
		tell window 1
			set foundButton to my findMoreButton(it)
			if foundButton is not missing value then
				click foundButton
			else
				display dialog "未找到描述为 'More' 的按钮。"
			end if
		end tell
	end tell
end tell

on findMoreButton(targetUIElement)
	tell application "System Events"
		-- 首先，在当前层级直接查找按钮
		try
			set moreButtons to (buttons of targetUIElement whose description is "More")
			if (count of moreButtons) > 0 then
				return first item of moreButtons
			end if
		on error
			-- 如果找不到按钮，继续
		end try
		
		-- 如果当前层级没有，则递归查找子 groups
		try
			set childGroups to (groups of targetUIElement)
			repeat with aGroup in childGroups
				set foundButton to my findMoreButton(aGroup)
				if foundButton is not missing value then
					return foundButton
				end if
			end repeat
		on error
			-- 如果没有子元素，继续
		end try
		
	end tell
	
	return missing value
end findMoreButton