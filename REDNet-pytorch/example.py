import argparse
import os
import io
import torch
import torch.backends.cudnn as cudnn
from torchvision import transforms
import PIL.Image as pil_image
from model import REDNet10, REDNet20, REDNet30

cudnn.benchmark = True
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def run_through_folder(directory):
    for filename in os.listdir(directory):
        filename = directory + "/" + filename
        if filename.endswith(".JPG") or filename.endswith(".jpg") or filename.endswith(".png"):

            input = pil_image.open(filename).convert('RGB')
            print(str(filename))
            filename = os.path.basename(filename).split('.')[0]

            buffer = io.BytesIO()
            input = transforms.ToTensor()(input).unsqueeze(0).to(device)

            with torch.no_grad():
                pred = model(input)

            pred = pred.mul_(255.0).clamp_(0.0, 255.0).squeeze(0).permute(1, 2, 0).byte().cpu().numpy()
            output = pil_image.fromarray(pred, mode='RGB')
            output.save(os.path.join(opt.outputs_dir, '{}.png'.format(filename)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--arch', type=str, default='REDNet10', help='REDNet10, REDNet20, REDNet30')
    parser.add_argument('--weights_path', type=str, required=True)
    parser.add_argument('--image_dir', type=str, required=True)
    parser.add_argument('--outputs_dir', type=str, required=True)
    parser.add_argument('--jpeg_quality', type=int, default=10)
    opt = parser.parse_args()

    if not os.path.exists(opt.outputs_dir):
        os.makedirs(opt.outputs_dir)

    if opt.arch == 'REDNet10':
        model = REDNet10()
    elif opt.arch == 'REDNet20':
        model = REDNet20()
    elif opt.arch == 'REDNet30':
        model = REDNet30()

    state_dict = model.state_dict()
    for n, p in torch.load(opt.weights_path, map_location=lambda storage, loc: storage).items():
        if n in state_dict.keys():
            state_dict[n].copy_(p)
        else:
            raise KeyError(n)

    model = model.to(device)
    model.eval()

    print(opt.image_dir)
    run_through_folder(opt.image_dir)
