# PROPOSED ADVERSARIAL TRAINING TOOLKIT INTERFACE
2024 06 24 Steven Chiacchira

## Attack
All attacks will have some common arguments:
- `seed`: int (torch random seed)

And return:
- The perturbed accuracy
- The perturbed loss
- The predicted labels
- The adversarial examples
---

This leaves a few questions:
- Do the attacks run over an entire dataset, or just a few examples? Do we allow both?
- What other information would we want to log, if any?

### APGD
Arguments:
- `p`: int | inf (attack norm)
- `loss`: "ce" | "dlr" (attack loss function)  // should probably be an `nn.Module` in order to keep this in line with `FGSM`
- `eps`: float (maximum perturbation)
- `iters`: int (number of iterations)

Do we want to include `rho` as a parameter? What does it mean?

### FGSM
Arguments:
- `eps`: float (maximum perturbation)
- `loss`: nn.Module (attack loss function)

Do we want to allow a targeted version of the attack? What about different norms (PGD *seems* to allow p=2).

### PGD
Arguments:
- `p`: 2 | inf (attack norm)
- `eps`: int (maximum perturbation)
- `iters`: int (number of iterations)
- `loss`: nn.Module (attack loss function)

Do we want to allow a targeted version of the attack?

---

What other attacks do we want to include? Off the top of my head I can think of:
- Carlini-Wagner
- Fool-X
- Target-X

## Defense
All adversarial training methods will require some common arguments:
- `batch_size`: int (number of examples per batch)
- `epochs`: int (number of training epochs)
- `checkpoint_epochs`: int (number of epochs per checkpoint)
- `lr`: float (learning rate)
- `model`: nn.Module (model being trained)  # might have to be an Enum with how the code is written

Additionally, we will need to track the following:
- Per epoch loss, accuracy, and possibly time
- Model checkpoints

It would be nice to allow the user to configure how often these are tracked and where they go (models and log files).

Some defenses allow the user to change between "cpu" and "cuda". We can do this, but I think it would be more trouble than it's worth. I cannot think of the last time I chose "cpu".

### ATAWP
Arguments:
- `p`: 2 | int (norm of the attack)
- `l1`: float (?)
- `l2`: float (?)
- `attack`: "pgd" | "fgsm" | "free" | "none" (?)
  - IF "fgsm" `fgsm_init`: "zero" | "random" | "previous"
- `eps`: float (?)
- `iters`: int (?)
- `half`: ? (?)
- `width_factor`: ? (?)
- `resume`: ? (?)
- `cutout`: ? (?)
- `cutout_len`: ? (?)
- `mixup`: ? (?)
  - IF "mixup" `mixup_alpha`: float (?)
- `val`: ? (?)
- `eval`: ? (?)
- `awp_gamma`: float (?)
- `awp_warmup`: int (?)
- `lr_scheduler`: "suprtconverge" | "piecewise" | "linear" | "piecewisesmoothed" | "piecewisezoom" | "onedrop" | "multipledecay" | "cosine" | "cyclic" (learning rate scheduler)

Should we consider adding `lr_scheduler` to other attacks? Is it specific to ATAWP? This attack also has `lr_max`; is that just the initial learning rate, or a ceiling?

### CURRAT (CAT?)
Arguments:
- `method`: "at" | "basic" | "cat" | "maxbm" | "nat" (?)
- `maxk`: int (?) // "method" notes "only batch mixing for max_k".
- `k`: int (?)
- `sgd`: bool (use stochastic gradient descent) // it might be better to just allow the choice of any optimizer?

### FAT
Arguments:
- `eps`: float (maximum perturbation)
- `momentum`: float (amount of momentum for optimizer)
- `omega`: float (?)  // documentation calls this "random sample parameter for adv data generation"
- `rand_init`: bool (whether to initialize the adversarial example with random noise)  // would you ever not switch this?
- `steps`: int (?) // documentation calls this "maximum perturbation step K"
- `step_size`: float (?) // related to "steps"?
- `tau`: int (?) // documentation calls this "step tau"
- `dynamictau`: bool (?)
- `weight_decay`: float (weight decay for optimizer)

This attack also has a number of parameters related to "WRN", which I presume to be "Wide Resnet":
- depth: int (?)
- width_factor: int (?)
- drop_rate: float (?) // dropout rate?
Should these be configured as part of the model?

Should we consider adding weight_decay or momentum for other attacks? Or are these specific to FAT?

### Feature Scatter
- `adv_mode`: "feature_scatter" (?) // this may be an artifact of an older architecture. Were we going to combine these parsers together at one point?
- `decay_epoch1`: int (?) // this could maybe be combined with "decay_epoch2", depending on what it is.
- `decay_epoch2`: int (?)
- `momentum`: float (amount of momentum for training)
- `num_classes`: int (?)  // if this is just the number of classes in the dataset (as opposed to the number considered by some algorithm) this should just be bundled with the dataset.
- `image_size`: tuple[int, int] (?) // if this is the size of dataset members it should just be bundled with the dataset

### GAIRAT
- `weight_decay`: float (weight decay for optimizer)
- `momentum`: float (momentum for optimizer)
- `steps`: int (?)  // documentations calls this "maximum perturbation step k"
- `step_size`: float (?)
- `random`: bool (whether to start adversarial examples as random)  // do we need this?
- `lr_scheduler`: "suprtconverge" | "piecewise" | "linear" | "piecewisesmoothed" | "piecewisezoom" | "onedrop" | "multipledecay" | "cosine" | "cyclic" (learning rate scheduler)
- `lambda`: str (?) // should this be a string type? Is this a form of regularization?
- `lambda_max`: "linear" | "piecewise" | "fixed" (lambda scheduler) // maybe this could share the "lr_scheduler" options for the user?
- `weight_assignment_function`: "discrete" | "sigmoid" | "tanh" (?)
- `begin_epoch`: int (first epoch for adversarial training)

This attack also has all of the Wide ResNet options from [FAT](#FAT).

Do we want to apply `lr_scheduler` to other defenses? What about `begin_epoch`?

<!-- ### LASAT


### OAAT


### TRADES


### TRADESAWP


### YOPO


### ADT++

-->


---

What kind of datasets and models do we want to allow? The current code *seems* to support the CIFAR10/CIFAR100 datasets and ResNet/WideResnet models. One of my concerns around expanding beyond this is that much of the code is hardcoded to allow only these specific models and datasets.
