// Remove existing iron ingot recipe
recipes.remove(<minecraft:iron_ingot>);

// Add new furnace recipe for iron ingot from iron ore
furnace.addRecipe(<minecraft:iron_ingot>, <minecraft:iron_ore>);

// Add shaped crafting recipe for iron block
recipes.addShaped(<minecraft:iron_block>, [
    [<minecraft:iron_ingot>, <minecraft:iron_ingot>, <minecraft:iron_ingot>],
    [<minecraft:iron_ingot>, <minecraft:iron_ingot>, <minecraft:iron_ingot>],
    [<minecraft:iron_ingot>, <minecraft:iron_ingot>, <minecraft:iron_ingot>]
]);

// Add shapeless crafting recipe to convert iron block back to ingots
recipes.addShapeless(<minecraft:iron_ingot> * 9, [<minecraft:iron_block>]);

// Remove all recipes that output diamond
recipes.removeByOutput(<minecraft:diamond>);

// Add ore dictionary entry
<ore:ingotIron>.add(<minecraft:iron_ingot>);
