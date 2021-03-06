# Generated by Django 3.1.4 on 2020-12-17 07:07

from django.db import migrations


def assign_tag_hunts(apps, schema_editor):
    # For existing tags, find the hunts of the puzzles they're associated with
    # If that's just one hunt, we're ok, but if it's more than one, we need to
    # create a copy of the tag for each other hunt and update the associations.
    PuzzleTag = apps.get_model("puzzles", "PuzzleTag")
    db_alias = schema_editor.connection.alias
    for tag in PuzzleTag.objects.using(db_alias).all():
        if tag.hunt_id:
            continue
        hunt_ids = list(tag.puzzles.values_list("hunt_id", flat=True).distinct())
        if hunt_ids:
            tag.hunt_id = hunt_ids[0]
            tag.save()
            for hunt_id in hunt_ids[1:]:
                new_tag = PuzzleTag(
                    hunt_id=hunt_id, name=tag.name, color=tag.color, is_meta=tag.is_meta
                )
                new_tag.save()
                for puzzle in tag.puzzles.filter(hunt_id=hunt_id):
                    puzzle.tags.remove(tag)
                    puzzle.tags.add(new_tag)
        else:
            tag.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("puzzles", "0017_auto_20201217_0626"),
    ]

    operations = [
        migrations.RunPython(assign_tag_hunts, migrations.RunPython.noop),
    ]
