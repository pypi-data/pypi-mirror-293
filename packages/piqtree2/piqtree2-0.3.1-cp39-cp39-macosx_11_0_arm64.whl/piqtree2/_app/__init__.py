"""cogent3 apps for piqtree2."""

from typing import Optional, Union

import cogent3
import cogent3.app.typing
from cogent3.app.composable import define_app
from cogent3.util.misc import extend_docstring_from

from piqtree2 import TreeGenMode, build_tree, fit_tree, random_trees
from piqtree2.model import Model


@define_app
@extend_docstring_from(build_tree)
def piqtree_phylo(
    aln: Union[cogent3.Alignment, cogent3.ArrayAlignment],
    model: Model,
    rand_seed: Optional[int] = None,
) -> Union[cogent3.PhyloNode, cogent3.app.typing.SerialisableType]:
    return build_tree(aln, model, rand_seed)


@define_app
@extend_docstring_from(fit_tree)
def piqtree_fit(
    aln: Union[cogent3.Alignment, cogent3.ArrayAlignment],
    tree: cogent3.PhyloNode,
    model: Model,
    rand_seed: Optional[int] = None,
) -> Union[cogent3.PhyloNode, cogent3.app.typing.SerialisableType]:
    return fit_tree(aln, tree, model, rand_seed)


@define_app
@extend_docstring_from(random_trees)
def piqtree_random_trees(
    num_taxa: int,
    tree_mode: TreeGenMode,
    num_trees: int,
    rand_seed: Optional[int] = None,
) -> tuple[cogent3.PhyloNode]:
    return random_trees(num_taxa, tree_mode, num_trees, rand_seed)


_ALL_APP_NAMES = ["piqtree_phylo", "piqtree_fit", "piqtree_random_trees"]
