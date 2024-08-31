import openfgl.config as config


from openfgl.flcore.trainer import FGLTrainer

args = config.args

args.root = "/Users/popo/work/openfgl_test"

args.dataset = ["Cora"]

args.model = ["gcn"]

args.metrics = ["accuracy"]

args.fl_algorithms = ["fedprox"]

trainer = FGLTrainer(args)

trainer.train()