extends KinematicBody2D

const UP = Vector2(0, -1)
const GRAVITY = 20
const ACCELERATION = 50
const MAX_SPEED = 200
const JUMP_HEIGHT = -500

var motion = Vector2()
var facing_right = true

func _physics_process(delta):
	motion.y += GRAVITY
	var friction = false

	if Input.is_action_pressed("ui_right"):
		motion.x = min(motion.x + ACCELERATION, MAX_SPEED)
		$Sprite.flip_h = false
		facing_right = true
	elif Input.is_action_pressed("ui_left"):
		motion.x = max(motion.x - ACCELERATION, -MAX_SPEED)
		$Sprite.flip_h = true
		facing_right = false
	else:
		friction = true

	if is_on_floor():
		if Input.is_action_just_pressed("ui_up"):
			motion.y = JUMP_HEIGHT
		if friction == true:
			motion.x = lerp(motion.x, 0, 0.2)
	else:
		if friction == true:
			motion.x = lerp(motion.x, 0, 0.05)

	if abs(motion.x) < 1:
		$Sprite.play("idle")
	else:
		$Sprite.play("run")

	if not is_on_floor():
		if motion.y < 0:
			$Sprite.play("jump")
		else:
			$Sprite.play("fall")

	motion = move_and_slide(motion, UP)

	if Input.is_action_just_pressed("ui_accept"):
		var bullet = preload("res://bullet.tscn").instance()
		bullet.set_bullet_direction(facing_right)
		bullet.position = $Position2D.global_position
		get_parent().add_child(bullet)
