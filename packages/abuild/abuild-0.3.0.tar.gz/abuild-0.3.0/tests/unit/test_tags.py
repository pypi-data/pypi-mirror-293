from abuild.tags import select_step


def describe_select_step():
    def should_be_true_for_empty_list():
        assert select_step('a', [])

    def should_be_true_if_step_in_list():
        assert select_step('a', ['a', 'b'])

    def should_be_false_if_step_is_not_in_list():
        assert not select_step('a', ['b', 'c'])

    def should_be_false_if_no_tag():
        assert not select_step(None, ['a', 'b'])

    def should_be_true_if_no_tag_is_explicitly_selected():
        assert select_step(':notag:', ['a', 'b', ':notag:'])

    def should_be_false_if_deselected():
        assert not select_step('a', ['!a'])

    def should_be_false_if_other_is_deselected():
        assert select_step('a', ['!b'])
