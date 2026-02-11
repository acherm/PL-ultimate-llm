// Simple Player Health System
// This script demonstrates basic TorqueScript features

function Player::onAdd(%this)
{
   %this.health = 100;
   %this.maxHealth = 100;
   %this.shield = 50;
   echo("Player created with health:" SPC %this.health);
}

function Player::takeDamage(%this, %amount)
{
   if (%this.shield > 0)
   {
      %shieldDamage = getMin(%amount, %this.shield);
      %this.shield -= %shieldDamage;
      %amount -= %shieldDamage;
      echo("Shield absorbed" SPC %shieldDamage SPC "damage");
   }

   if (%amount > 0)
   {
      %this.health -= %amount;
      echo("Player took" SPC %amount SPC "damage");
   }

   if (%this.health <= 0)
   {
      %this.onDeath();
   }
}

function Player::heal(%this, %amount)
{
   %this.health = getMin(%this.health + %amount, %this.maxHealth);
   echo("Player healed to" SPC %this.health);
}

function Player::onDeath(%this)
{
   echo("Player has died!");
   %this.health = 0;
}

function Player::getHealthPercent(%this)
{
   return (%this.health / %this.maxHealth) * 100;
}
