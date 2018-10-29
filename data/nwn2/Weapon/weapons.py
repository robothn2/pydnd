#coding: utf-8
from Models import register_weapon

def register(protos):
    # Simple weapon
    register_weapon(protos, 'Club',
                    damageRoll=(1,6),       # 1d6
                    criticalThreat=(2,2),   # 19-20/x2
                    damageType=('Bludgeoning'), size='Medium', feat='Simple', weight=3.0,
                    specifics='''The club is a very basic weapon, usually consisting of nothing more than a tapered length of hardwood.''')
    register_weapon(protos, 'Dagger',
                    damageRoll=(1,4), criticalThreat=(3,2), damageType=('Piercing'), size='Tiny', feat='Simple', weight=1.0,
                    specifics='''A basic but versatile weapon, the dagger consists of a double-edged piercing blade that typically ranges from about 6 to 24 inches in length.''')
    register_weapon(protos, 'Dart',
                    damageRoll=(1,4), criticalThreat=(2,2), damageType=('Piercing'), size='Tiny', feat='Simple', weight=0.0,
                    specifics='''These missile weapons are close in size to a small dagger, and are hurled in combat toward their target.''')
    register_weapon(protos, 'Heavy Crossbow',
                    damageRoll=(1,10), criticalThreat=(3,2), damageType=('Piercing'), size='Medium', feat='Simple', weight=8.0,
                    specifics='''The heavy crossbow is the largest hand-held launcher of its type, and is favored by militia groups for its durability and ease of use. It is deadlier than its smaller cousin, but also more cumbersome.''')
    register_weapon(protos, 'Light Crossbow',
                    damageRoll=(1,8), criticalThreat=(3,2), damageType=('Piercing'), size='Small', feat='Simple', weight=4.0,
                    specifics='''The crossbow resembles a bow laid crosswise on a wood or metal shaft, and is favored for its versatility. The light crossbow variant is durable and reasonably easy to conceal, but lacks some of the punch of its larger cousin.''')
    register_weapon(protos, 'Mace',
                    damageRoll=(1,6), criticalThreat=(2,2), damageType=('Bludgeoning'), size='Small', feat='Simple', weight=4.0,
                    specifics='''The mace is a derivative of the basic club, consisting of a stone or metal head mounted on the end of a wooden shaft. The weight of the head greatly increases the force of impact.''')
    register_weapon(protos, 'Morningstar',
                    damageRoll=(1,8), criticalThreat=(2,2), damageType=('Bludgeoning'), size='Medium', feat='Simple', weight=6.0,
                    specifics='''The morningstar is a derivative of the mace that includes a chain tether - similar to the flail - to add velocity when swinging its compact striking surface. Morningstars commonly have at least one formidable spike as an added feature of the head.''')
    register_weapon(protos, 'Quarterstaff',
                    damageRoll=(1,6), criticalThreat=(2,2), damageType=('Bludgeoning'), size='Large', feat='Simple', weight=4.0,
                    specifics='''Usually crafted of hardwood and occasionally shod with metal at either end, the quarterstaff is a humble weapon that almost anyone can learn to use effectively.''')
    register_weapon(protos, 'Sickle',
                    damageRoll=(1,6), criticalThreat=(2,2), damageType=('Slashing'), size='Small', feat='Simple', weight=2.0,
                    specifics='''The sickle is a farming implement used for cutting grass and grains. Like many other such tools, it was adapted for use as a weapon by the peasants familiar with it in their daily toils.''')
    register_weapon(protos, 'Sling',
                    damageRoll=(1,4), criticalThreat=(2,2), damageType=('Bludgeoning'), size='Small', feat='Simple', weight=0.1,
                    specifics='''The sling is an ancient weapon; a simple construction that is little more than a small pouch attached to a leather or fabric strip, and combined with suitable ammunition.''')
    register_weapon(protos, 'Spear',
                    damageRoll=(1,8), criticalThreat=(2,3), damageType=('Piercing'), size='Large', feat='Simple', weight=6.0,
                    specifics='''Another of history's most basic weapons, the spear is nevertheless a formidable weapon. Little more that a simple shaft topped with a sharpened head, the spear is the staple of many a militia.''')


    # Martial weapon
    register_weapon(protos, 'Battleaxe',
                   damageRoll=(1,8), criticalThreat=(2,3), damageType=('Slashing'), size='Medium', feat='Martial', weight=6.0,
                   specifics='''The battleaxe consists of a single blade atop a three- or four-foot shaft. It is a versatile weapon, and remains a useful tool when not in combat.''')
    register_weapon(protos, 'Falchion',
                   damageRoll=(2,4), criticalThreat=(4,2), damageType=('Slashing'), size='Large', feat='Martial', weight=8.0,
                   specifics='''This sword, which is essentially a two-handed scimitar, has a curve that gives it the effect of a keener edge.''')
    register_weapon(protos, 'Flail',
                   damageRoll=(1,8), criticalThreat=(2,2), damageType=('Bludgeoning'), size='Medium', feat='Martial', weight=5.0,
                   specifics='''Originally a farm implement for threshing grain, the flail consists of a wooden shaft attached to a heavy or spiked head by a chain or hinge. The flail is approximately two feet long.''')
    register_weapon(protos, 'Greataxe',
                   damageRoll=(1,12), criticalThreat=(2,3), damageType=('Slashing'), size='Large', feat='Martial', weight=12.0,
                   specifics='''A favorite of barbarians, the greataxe is the largest of the weapons derived from the basic woodcutter's axe. The double-edged head is far more suited to cleaving opponents than trees.''')
    register_weapon(protos, 'Greatsword',
                   damageRoll=(2,6), criticalThreat=(3,2), damageType=('Slashing','Piercing'), size='Large', feat='Martial', weight=8.0,
                   specifics='''The greatsword is an impressive weapon by any measure, and is held with two hands by all but the largest of creatures.''')
    register_weapon(protos, 'Halberd',
                   damageRoll=(1,10), criticalThreat=(2,3), damageType=('Slashing','Piercing'), size='Large', feat='Martial', weight=12.0,
                   specifics='''The halberd is the most common polearm, and could be called a cross between a spear and an axe. Such weapons are often mass-produced for militia, and serve well when defending against marauders.''')
    register_weapon(protos, 'Handaxe',
                   damageRoll=(1,6), criticalThreat=(2,3), damageType=('Slashing'), size='Small', feat='Martial', weight=3.0,
                   specifics='''The handaxe is smaller than most axes used for combat, and is most often used as an off-hand weapon.''')
    register_weapon(protos, 'Kukri',
                   damageRoll=(1,4), criticalThreat=(4,2), damageType=('Slashing'), size='Tiny', feat='Martial', weight=2.0,
                   specifics='''Kukri are heavy, curved daggers with their sharpened edge on the inside arc of the blade. This type of weapon has its roots as a tool, but has been heavily adapted to ritual and warfare.''')
    register_weapon(protos, 'Light Hammer',
                   damageRoll=(1,4), criticalThreat=(2,2), damageType=('Bludgeoning'), size='Small', feat='Martial', weight=2.0,
                   specifics='''The light hammer is derived from commonly used mining tools. It remains small enough to still be used in excavation, unlike the much heavier warhammer.''')
    register_weapon(protos, 'Longbow',
                   damageRoll=(1,8), criticalThreat=(2,3), damageType=('Piercing'), size='Large', feat='Martial', weight=3.0,
                   specifics='''The longbow is a refinement of the shortbow, designed to increase the range and power of an arrow strike. The stave portion of a longbow is nearly as tall as the archer, and can reach over six feet.''')
    register_weapon(protos, 'Longsword',
                   damageRoll=(1,8), criticalThreat=(3,2), damageType=('Slashing','Piercing'), size='Medium', feat='Martial', weight=4.0,
                   specifics='''The longsword is the weapon most commonly associated with knights and their ilk. There are many variations in the blade, but all are approximately 35 to 47 inches in length.''')
    register_weapon(protos, 'Rapier',
                   damageRoll=(1,6), criticalThreat=(4,2), damageType=('Piercing'), size='Medium', feat='Martial', weight=2.0,
                   specifics='''The rapier is a light, thrusting sword popular among nobles and swashbucklers. Often associated with dueling and sport fighting, rapiers are nonetheless deadly in trained hands.''')
    register_weapon(protos, 'Scimitar',
                   damageRoll=(1,6), criticalThreat=(4,2), damageType=('Slashing'), size='Medium', feat='Martial', weight=4.0,
                   specifics='''The scimitar shares some similarities with the longsword and other slashing blades, but the severity and thickness of its curve clearly sets it apart.''')
    register_weapon(protos, 'Scythe',
                   damageRoll=(2,4), criticalThreat=(2,4), damageType=('Slashing','Piercing'), size='Large', feat='Martial', weight=10.0,
                   specifics='''While obviously resembling the farm implement it is derived from, a scythe built for war is reinforced to withstand the rigors of combat.''')
    register_weapon(protos, 'Short Sword',
                   damageRoll=(1,6), criticalThreat=(3,2), damageType=('Piercing'), size='Small', feat='Martial', weight=2.0,
                   specifics='''One of the first types of sword to come into existence, the short sword is a double-edged weapon about two feet long. It is an economical weapon, and a favorite of archers and rogues.''')
    register_weapon(protos, 'Shortbow',
                   damageRoll=(1,6), criticalThreat=(2,3), damageType=('Piercing'), size='Medium', feat='Martial', weight=2.0,
                   specifics='''A shortbow has a stave portion of about five feet in length. The shortbow was the first of such launchers to be developed, and it remains an effective weapon.''')
    register_weapon(protos, 'Throwing Axe',
                   damageRoll=(1,6), criticalThreat=(2,2), damageType=('Slashing'), size='Tiny', feat='Martial', weight=0.0,
                   specifics='''The throwing axe bears little in common with the farm implement it is derived from. It has been carefully balanced for flight, sacrificing durability for precision.''')
    register_weapon(protos, 'Warhammer',
                   damageRoll=(1,8), criticalThreat=(2,3), damageType=('Bludgeoning'), size='Medium', feat='Martial', weight=5.0,
                   specifics='''Originally adapted from the tools of laborers and craftsmen, the warhammer is a far-heavier variant of the sledge and is no longer suitable for anything but combat.''')
    register_weapon(protos, 'Warmace',
                   damageRoll=(1,12), criticalThreat=(2,2), damageType=('Bludgeoning'), size='Large', feat='Martial', weight=9.0,
                   specifics='''Top-heavy and unwieldy the warmace is a larger variant of the common footman's mace that sacrifices elegance for effectiveness.''')


    # Exotic weapon
    register_weapon(protos, 'Bastard Sword',
                   damageRoll=(1,10), criticalThreat=(3,2), damageType=('Slashing', 'Piercing'), size='Medium', feat='Exotic', weight=6.0,
                   specifics='''Bastard swords are also known as hand-and-a-half swords, falling between the longsword and greatsword in length.''')
    register_weapon(protos, 'Dwarven Waraxe',
                   damageRoll=(1,10), criticalThreat=(2,3), damageType=('Slashing'), size='Medium', feat='Exotic', weight=8.0,
                   specifics='''A dwarven waraxe is much like the dwarves themselves; strong, hardy and very brutal.''')
    register_weapon(protos, 'Kama',
                   damageRoll=(1,6), criticalThreat=(2,2), damageType=('Slashing'), size='Small', feat='Exotic', weight=2.0,
                   specifics='''As with many weapons, the kama was adapted for combat by the peasants that used them as farming implements, often because they were forbidden from owning swords or the like.''')
    register_weapon(protos, 'Katana',
                   damageRoll=(1,10), criticalThreat=(3,2), damageType=('Slashing', 'Piercing'), size='Medium', feat='Exotic', weight=5.0,
                   specifics='''The katana is the pinnacle of the swordsmith's craft, combining grace and artful design with razor-edged efficiency.''')
    register_weapon(protos, 'Shuriken',
                   damageRoll=(1,3), criticalThreat=(2,2), damageType=('Piercing'), size='Tiny', feat='Exotic', weight=0.0,
                   specifics='''Shuriken are light, easy to conceal, and while they do little damage individually, they can be thrown very quickly.''')

