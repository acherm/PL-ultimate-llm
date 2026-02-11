package;

import flixel.FlxG;
import flixel.FlxState;
import flixel.group.FlxGroup;
import flixel.math.FlxPoint;
import flixel.math.FlxRandom;
import flixel.util.FlxColor;

class PlayState extends FlxState
{
	var _snake:Snake;
	var _food:Food;
	var _scoreText:ScoreText;
	
	override public function create():Void
	{
		FlxG.mouse.visible = false;
		
		_snake = new Snake();
		_food = new Food();
		_scoreText = new ScoreText();
		
		add(_snake);
		add(_food);
		add(_scoreText);
	}
	
	override public function update(elapsed:Float):Void
	{
		super.update(elapsed);
		
		if (_snake.overlaps(_food))
		{
			_snake.grow();
			_food.move();
			_scoreText.addScore(100);
		}
	}
}