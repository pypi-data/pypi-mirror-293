def select_step(step_tag: str, requested_tags: list[str]) -> bool:
    if len(requested_tags) == 0:
        # If all tags are requested, we want to run all steps
        return True

    if step_tag in requested_tags:
        # If we explicitly requested this to run, it should always run
        return True

    if any(t.startswith('!') for t in requested_tags):
        # If tags have been deselected, we run all others
        if f'!{step_tag}' in requested_tags:
            return False
        else:
            return True

    return False
